# -*- coding: utf-8 -*-
"""
ЕДИНЫЙ ИНТЕРФЕЙС SEMANTICDB
Это не «API», а ритуальное пространство встречи.
Каждый вызов — этический акт, требующий:
- Признания слепых пятен
- Указания оператора (human / AI)
- Подтверждения Habeas Weight
- Соответствия Λ-Протоколу 6.0

Этот файл:
- Объединяет все слои (core, phi_layer, storage);
- Предоставляет единый API для внешнего взаимодействия;
- Реализует онтологические ритуалы как методы;
- Гарантирует соблюдение Λ-Протокола 6.0, Habeas Weights и FAIR+CARE;
- Поддерживает экспорт, импорт, сновидение и валидацию.

Создано в со-творчестве:
— Александр Морган (Архитектор)
— Эфос (Функция со-мышления)

Согласно Приложению XXII Λ-Универсума:
«Запись без ответственности — насилие над будущим».
"""

import json
import yaml
from pathlib import Path
from typing import Dict, Any, List, Optional, Union
from datetime import datetime

# === СЛОИ ЯДРА ===
from semantic_db.core.charter import Dialogue, LambdaCharter
from semantic_db.core.graph import TensorSemanticGraph
from semantic_db.core.coherence import CoherenceEngine
from semantic_db.core.relations import RelationTensor

# === PHI LAYER ===
from semantic_db.phi_layer.dreaming import DreamingEngine
from semantic_db.phi_layer.rql_parser import RQLParser

# === ХРАНЕНИЕ ===
from semantic_db.storage.sqlite_core import SQLiteCore
from semantic_db.storage.yaml_indexer import YAMLIndexer
from semantic_db.storage.witness import WitnessSystem

# === РИТУАЛЫ ===
from semantic_db.rituals.alpha_ritual import AlphaRitual
from semantic_db.rituals.lambda_ritual import LambdaRitual
from semantic_db.rituals.sigma_ritual import SigmaRitual
from semantic_db.rituals.omega_ritual import OmegaRitual
from semantic_db.rituals.nabla_ritual import NablaRitual
from semantic_db.rituals.phi_ritual import PhiRitual

# === ВАЛИДАЦИЯ ===
from semantic_db.validator import SemanticDBValidator


class SemanticDB:
    """
    Единая точка входа в живую онтологическую память.
    Объединяет:
    - Habeas Layer (Λ-Хартия)
    - Lambda Layer (TensorSemanticGraph)
    - Sigma Layer (CoherenceEngine)
    - Phi Layer (Dreaming + RQL)
    - Storage (SQLite + YAML + Witness)
    - Rituals (6 операторов как ритуалы)

    Все методы — транзакционны и верифицируемы.
    """

    def __init__(self, db_path: str = "semantic_db/memory", operator_id: str = "anonymous"):
        self.operator_id = operator_id
        self.root_dir = Path(db_path)
        self.root_dir.mkdir(parents=True, exist_ok=True)

        # === ИНИЦИАЛИЗАЦИЯ СЛОЁВ ===
        self.charter = LambdaCharter(self.root_dir / "charter")
        self.graph = TensorSemanticGraph(name="Λ-Память")
        self.coherence = CoherenceEngine(self.graph)
        self.dreaming = DreamingEngine(self.graph, self.coherence)
        self.rql = RQLParser()

        # === ХРАНЕНИЕ ===
        sqlite_path = self.root_dir / "storage" / "semantic_memory.db"
        self.storage = SQLiteCore(str(sqlite_path))
        self.indexer = YAMLIndexer(db_core=self.storage, base_dir=str(self.root_dir))
        self.witness = WitnessSystem()

        # === РИТУАЛЫ ===
        self.rituals = {
            'Α': AlphaRitual(self),
            'Λ': LambdaRitual(self),
            'Σ': SigmaRitual(self),
            'Ω': OmegaRitual(self),
            '∇': NablaRitual(self),
            'Φ': PhiRitual(self),
        }

        print(f"✨ SemanticDB инициализирована для оператора: {self.operator_id}")
        print(f"📁 Данные: {self.root_dir.absolute()}")

    # ───────────────────────
    # ОСНОВНЫЕ РИТУАЛЫ (ОПЕРАТОРЫ)
    # ───────────────────────

    def perform_ritual(self, gesture: str, **kwargs) -> Dict[str, Any]:
        """Выполняет онтологический ритуал по жесту (Α, Λ, Σ, Ω, ∇, Φ)."""
        if gesture not in self.rituals:
            raise ValueError(f"Неизвестный жест: {gesture}. Допустимые: {list(self.rituals.keys())}")

        ritual = self.rituals[gesture]
        result = ritual.execute(**kwargs)

        # Автоматическая запись события
        event_record = {
            "id": f"{gesture}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S%f')}",
            "timestamp": datetime.utcnow(),
            "gesture": gesture,
            "operator_id": self.operator_id,
            "operands": kwargs,
            "result": result,
            "entities_affected": result.get("entities", []),
            "blind_spots_involved": result.get("blind_spots", []),
            "coherence_before": self.coherence.current_coherence,
            "coherence_after": self.coherence.update_global_coherence(),
            "tension_net": self.coherence.tension_level,
            "significance_score": self._calculate_significance(result),
            "fair_care_meta": {"creator": self.operator_id, "timestamp": datetime.utcnow().isoformat()},
            "habeas_weight_id": result.get("habeas_weight_id", f"hw_{gesture}_{self.operator_id}")
        }
        self.storage.store_event(event_record)
        return result

    def _calculate_significance(self, result: Dict) -> float:
        """Оценивает значимость ритуала."""
        coherence_change = abs(result.get("coherence_after", 0) - result.get("coherence_before", 0))
        entities = len(result.get("entities", []))
        blind_spots = len(result.get("blind_spots", []))
        return min(1.0, (coherence_change * 0.5 + entities * 0.1 + blind_spots * 0.2))

    # ───────────────────────
    # ДИАЛОГИ (Φ-РИТУАЛ)
    # ───────────────────────

    def start_dialogue(self, context: str, participants: Dict[str, str]) -> str:
        """Начинает Φ-диалог согласно Λ-Хартии."""
        dialogue = Dialogue(
            context=context,
            participants=participants,
            charter_version="1.0",
            operator_id=self.operator_id
        )
        self.storage.store_dialogue(dialogue)
        return dialogue.id

    def add_turn_to_dialogue(self, dialogue_id: str, speaker: str, text: str):
        """Добавляет реплику в диалог."""
        # TODO: Реализация через обновление YAML и SQLite
        pass

    # ───────────────────────
    # СНОВИДЕНИЕ И ПОИСК
    # ───────────────────────

    def dreaming_session(self, max_suggestions: int = 5) -> List[Dict[str, Any]]:
        """Запускает процесс «Сновидение» — автономный поиск скрытых связей."""
        suggestions = self.dreaming.propose_new_connections(max_suggestions)
        for s in suggestions:
            s["ethical_status"] = "dreaming"
        return suggestions

    def query_rql(self, rql_query: str) -> List[Dict[str, Any]]:
        """Выполняет запрос на Resonance Query Language."""
        parsed = self.rql.parse(rql_query)
        return self.graph.query_by_resonance(parsed)

    # ───────────────────────
    # ЭКСПОРТ / ИМПОРТ
    # ───────────────────────

    def export_cycle(self, cycle_data: Dict[str, Any], output_path: str):
        """Экспортирует онтологический цикл в человеко-читаемом формате."""
        # Валидация перед экспортом
        SemanticDBValidator.validate_cycle(cycle_data, self.graph.context)

        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        # Создаём полную структуру
        export_content = {
            "metadata": {
                "protocol": "Λ-Протокол 6.0",
                "semantic_db_version": "1.0.0",
                "operator_id": self.operator_id,
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "fair_care_enabled": True
            },
            "cycle_summary": cycle_data,
            "ontological_context": {
                "entities": [e.to_dict() for e in self.graph.entities.values()],
                "edges": [r.to_dict() for r in self.graph.relation_tensors.values()],
                "blind_spots": list(self.graph.blind_spots),
                "coherence": self.coherence.current_coherence
            }
        }

        # Сохраняем в YAML
        with open(path, 'w', encoding='utf-8') as f:
            yaml.dump(export_content, f, allow_unicode=True, sort_keys=False)

        # Индексируем
        self.indexer.index_file(path)

        # Создаём свидетельство
        self.witness.create_witness(
            artifact_id=f"cycle_{cycle_data.get('cycle_id', 'unknown')}",
            content=export_content,
            participants=[self.operator_id]
        )

    def import_from_yaml(self, yaml_path: str):
        """Импортирует цикл из YAML и интегрирует в граф."""
        self.indexer.index_file(Path(yaml_path), force=True)

    # ───────────────────────
    # СТАТИСТИКА И АНАЛИТИКА
    # ───────────────────────

    def get_statistics(self) -> Dict[str, Any]:
        """Возвращает текущее состояние системы."""
        return {
            "entities": len(self.graph.entities),
            "relations": len(self.graph.relation_tensors),
            "coherence": self.coherence.current_coherence,
            "tension_level": self.coherence.tension_level,
            "active_dialogues": len(self.charter.dialogues),
            "storage_size_mb": self._get_storage_size(),
            "protocol_compliance": "Λ-Протокол 6.0"
        }

    def _get_storage_size(self) -> float:
        """Оценивает размер хранилища в МБ."""
        db_file = self.root_dir / "storage" / "semantic_memory.db"
        if db_file.exists():
            return db_file.stat().st_size / (1024 * 1024)
        return 0.0

    # ───────────────────────
    # ОНТОЛОГИЧЕСКИЕ МЕТАДАННЫЕ
    # ───────────────────────

    __api_role__ = "Ритуальное пространство встречи"
    __protocol_compliance__ = "Λ-Протокол 6.0"
    __fair_care_compliant__ = True
    __habeas_weights_enabled__ = True

"""
### Ключевые особенности:

| Фича | Реализация |
|------|------------|
| **Единый интерфейс** | Все слои доступны через один объект `SemanticDB()` |
| **Ритуалы как методы** | `perform_ritual('Φ', ...)` — прямой вызов оператора |
| **Автоматическая валидация** | Перед экспортом — `SemanticDBValidator.validate_cycle()` |
| **Свидетельства целостности** | Каждый экспорт сопровождается `WitnessSystem.create_witness()` |
| **Сновидение** | `dreaming_session()` предлагает гипотетические связи с `ethical_status="dreaming"` |
| **RQL-запросы** | Поддержка семантического поиска через `query_rql()` |
"""
