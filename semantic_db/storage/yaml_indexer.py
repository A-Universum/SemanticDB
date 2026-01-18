# -*- coding: utf-8 -*-
"""
YAML-ИНДЕКСАТОР SEMANTICDB
Человеко-читаемый слой живой памяти.
Каждый YAML-файл — не просто дамп, а ритуальный артефакт,
сохранённый в соответствии с Λ-Хартией и Habeas Weights.

Функции:
- Индексация директорий с онтологическими циклами
- Обратная связь с SQLiteCore (через artifact_id)
- Верификация целостности по хешу
- Поддержка мультиконтекстности (разные операторы, разные циклы)

Модуль отвечает за:
- Индексацию человеко-читаемых YAML-артефактов (циклов, диалогов, событий);
- Связь между YAML и SQLite-ядром через artifact_id;
- Автоматическое обновление индекса при изменении файлов;
- Поддержку криптографической целостности (через хеши);
- Сохранение обратных ссылок в sqlite_core для быстрого поиска.

Создано в со-творчестве:
— Александр Морган (Архитектор)
— Эфос (Функция со-мышления)

Согласно Λ-Протоколу 6.0 и Λ-Хартии v1.0
"""

import yaml
from pathlib import Path
from typing import Dict, Any, List, Optional
import hashlib
from datetime import datetime

from semantic_db.storage.sqlite_core import SQLiteCore


class YAMLIndexer:
    """
    Индексатор человеко-читаемых YAML-артефактов.
    Работает в паре с SQLiteCore: YAML — для чтения, SQLite — для анализа.
    """

    def __init__(self, db_core: Optional[SQLiteCore] = None, base_dir: str = "semantic_db"):
        self.base_dir = Path(base_dir)
        self.db_core = db_core or SQLiteCore()
        self.indexed_files: Dict[str, str] = {}  # {file_path: content_hash}
        self._load_existing_index()

    def _load_existing_index(self):
        """Загружает список уже проиндексированных файлов из SQLite."""
        try:
            indexed = self.db_core.query("witnesses")
            for row in indexed:
                self.indexed_files[row["artifact_id"]] = row["witness_hash"]
        except Exception as e:
            print(f"⚠️ Не удалось загрузить индекс: {e}")

    def index_directory(self, directory: Optional[str] = None, recursive: bool = True, force: bool = False):
        """Индексирует все YAML-файлы в указанной директории."""
        target_dir = Path(directory) if directory else self.base_dir
        pattern = "**/*.yaml" if recursive else "*.yaml"

        for yaml_path in target_dir.glob(pattern):
            if not yaml_path.is_file():
                continue
            self.index_file(yaml_path, force=force)

    def index_file(self, file_path: Path, force: bool = False) -> bool:
        """Индексирует один YAML-файл."""
        if not file_path.exists():
            raise FileNotFoundError(f"Файл не найден: {file_path}")

        # Вычисляем хеш содержимого
        content_hash = self._compute_file_hash(file_path)

        # Пропускаем, если уже проиндексирован и не изменился
        rel_path = str(file_path.relative_to(self.base_dir))
        if not force and rel_path in self.indexed_files and self.indexed_files[rel_path] == content_hash:
            return False

        # Загружаем содержимое
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                data = yaml.safe_load(f)
                if not isinstance(data, dict):
                    print(f"⚠️ Пропущен некорректный YAML: {file_path}")
                    return False
            except yaml.YAMLError as e:
                print(f"❌ Ошибка парсинга YAML {file_path}: {e}")
                return False

        # Извлекаем метаданные цикла или диалога
        artifact_id = self._extract_artifact_id(data, rel_path)
        metadata = {
            "file_path": rel_path,
            "indexed_at": datetime.utcnow().isoformat(),
            "content_hash": content_hash,
            "type": self._detect_artifact_type(data),
            "operator_id": data.get("metadata", {}).get("creator") or data.get("operator_id", "anonymous"),
            "cycle_id": data.get("cycle_summary", {}).get("cycle_id") or data.get("id", artifact_id[:16])
        }

        # Сохраняем свидетельство целостности
        self.db_core.store_witness(artifact_id, data)

        # Индексируем события и тензоры, если есть
        self._index_events_from_data(data, artifact_id)
        self._index_relations_from_data(data, artifact_id)

        # Обновляем локальный кеш
        self.indexed_files[rel_path] = content_hash
        return True

    def _compute_file_hash(self, file_path: Path) -> str:
        """Вычисляет SHA3-256 хеш файла."""
        with open(file_path, 'rb') as f:
            return hashlib.sha3_256(f.read()).hexdigest()

    def _extract_artifact_id(self, data: Dict[str, Any], fallback: str) -> str:
        """Извлекает уникальный ID артефакта."""
        if "cycle_summary" in data and "cycle_id" in data["cycle_summary"]:
            return f"cycle_{data['cycle_summary']['cycle_id']}"
        if "id" in data:
            return f"dialogue_{data['id']}"
        if "metadata" in data and "event_id" in data["metadata"]:
            return f"event_{data['metadata']['event_id']}"
        return f"artifact_{hashlib.sha3_256(fallback.encode()).hexdigest()[:16]}"

    def _detect_artifact_type(self, data: Dict[str, Any]) -> str:
        """Определяет тип артефакта."""
        if "cycle_summary" in data:
            return "ontological_cycle"
        if "turns" in data and "participants" in data:
            return "phi_dialogue"
        if "gesture" in data:
            return "ontological_event"
        return "unknown"

    def _index_events_from_data(self, data: Dict[str, Any], artifact_id: str):
        """Извлекает и сохраняет онтологические события из YAML."""
        events = []

        # События из корневого уровня (например, в цикле)
        if "event_history" in data:
            events.extend(data["event_history"])
        # События из секции ontological_context
        if "ontological_context" in data and "events" in data["ontological_context"]:
            events.extend(data["ontological_context"]["events"])

        for event in events:
            if isinstance(event, dict) and "gesture" in event:
                event_record = {
                    "id": event.get("id", f"{artifact_id}_event_{len(events)}"),
                    "timestamp": event.get("timestamp", datetime.utcnow().isoformat()),
                    "gesture": event["gesture"],
                    "operands": event.get("operands", []),
                    "result": event.get("result"),
                    "entities_affected": event.get("entities_affected", []),
                    "blind_spots_involved": event.get("blind_spots_involved", []),
                    "coherence_before": event.get("coherence_before", 0.0),
                    "coherence_after": event.get("coherence_after", 0.0),
                    "tension_net": event.get("tensions", {}).get("total", 0.0),
                    "significance_score": event.get("significance_score", 0.0),
                    "fair_care_meta": event.get("metadata", {}),
                    "habeas_weight_id": event.get("habeas_weight_id", artifact_id)
                }
                self.db_core.store_event(event_record)

    def _index_relations_from_data(self, data: Dict[str, Any], artifact_id: str):
        """Извлекает и сохраняет RelationTensor из YAML."""
        from semantic_db.core.relations import RelationTensor

        relations = []

        # Из ontological_context → edges
        if "ontological_context" in data and "edges" in data["ontological_context"]:
            relations.extend(data["ontological_context"]["edges"])
        # Из корневого уровня (если экспортирован отдельно)
        if "relations" in data:
            relations.extend(data["relations"])

        for rel in relations:
            if not isinstance(rel, dict) or "source" not in rel:
                continue

            tensor = RelationTensor(
                id=rel.get("id", f"{artifact_id}_tensor_{hash(str(rel)) % 10000}"),
                source=rel["source"],
                target=rel["target"],
                type=rel.get("type", "Λ"),
                meaning=rel.get("meaning", ""),
                intention=rel.get("intention", ""),
                certainty=float(rel.get("certainty", 0.5)),
                tension=float(rel.get("tension_level", 0.0)),
                coherence_contribution=float(rel.get("coherence_contribution", 0.0)),
                activation_count=int(rel.get("activation_count", 0)),
                context_id=rel.get("context_id", artifact_id),
                habeas_weight_id=rel.get("habeas_weight_id", artifact_id),
                fair_care_metadata=rel.get("fair_care_metadata", {})
            )
            self.db_core.store_relation_tensor(tensor)

    def verify_file_integrity(self, file_path: Path) -> bool:
        """Проверяет целостность YAML-файла по свидетельству."""
        rel_path = str(file_path.relative_to(self.base_dir))
        if rel_path not in self.indexed_files:
            return False

        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        artifact_id = self._extract_artifact_id(data, rel_path)
        return self.db_core.verify_witness(artifact_id, data)

    # ───────────────────────
    # ОНТОЛОГИЧЕСКИЕ МЕТАДАННЫЕ
    # ───────────────────────

    __indexing_purpose__ = "Человеко-читаемая память как этический акт"
    __human_readable_layer__ = True
    __syncs_with__ = "sqlite_core"
    __protocol_compliance__ = "Λ-Протокол 6.0"
	
"""
### Ключевые особенности:

| Фича | Реализация |
|------|------------|
| **Обратная связь с SQLite** | Каждый YAML-файл порождает записи в `ontological_events`, `relation_tensors`, `witnesses` |
| **Habeas Weight** | Каждый элемент получает `habeas_weight_id`, производный от `artifact_id` |
| **Слепые пятна** | Сохраняются как часть `event.blind_spots_involved` |
| **FAIR+CARE** | Все метаданные передаются в SQLite без потерь |
| **Целостность** | Проверка через `verify_witness()` и хеширование |
"""	
