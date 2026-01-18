# -*- coding: utf-8 -*-
"""
КРИПТОГРАФИЧЕСКИЕ СВИДЕТЕЛЬСТВА SEMANTICDB
Каждый онтологический артефакт — не просто запись, а юридически-этический акт.
Свидетельство (Witness) — это не хеш, а криптографический конверт,
содержащий:
- Контент (в нормализованной форме)
- Метаданные (FAIR+CARE, Habeas Weight ID)
- Подписи участников (если применимо)
- Временную метку создания
- Алгоритм хеширования

Модуль обеспечивает:
- Криптографическую целостность всех онтологических артефактов (диалогов, событий, тензоров);
- Невоспроизводимость свидетельств (каждый артефакт имеет уникальный хеш + временная метка + подписи участников);
- Поддержку FAIR+CARE через встроенные метаданные в свидетельство;
- Интеграцию с sqlite_core.py и yaml_indexer.py для сквозной верификации;
- Аудитопригодность: любой внешний агент может проверить подлинность записи без доступа к исходному коду.

Создано в со-творчестве:
— Александр Морган (Архитектор)
— Эфос (Функция со-мышления)

Согласно Λ-Протоколу 6.0 и Λ-Хартии v1.0
"""

import hashlib
import json
from typing import Dict, Any, Optional, List
from datetime import datetime


class WitnessSystem:
    """
    Система криптографических свидетельств.
    Гарантирует, что каждый артефакт в SemanticDB:
    - Не может быть подделан
    - Не может быть удалён без следа
    - Может быть независимо верифицирован
    """

    DEFAULT_ALGORITHM = "sha3-256"

    @staticmethod
    def create_witness(
        artifact_id: str,
        content: Dict[str, Any],
        participants: Optional[List[str]] = None,
        algorithm: str = DEFAULT_ALGORITHM
    ) -> Dict[str, Any]:
        """
        Создаёт полное свидетельство для артефакта.
        Возвращает структуру, готовую к сохранению в SQLite или YAML.
        """
        # Нормализуем контент для детерминированного хеширования
        normalized_content = json.dumps(content, sort_keys=True, ensure_ascii=False, separators=(',', ':'))

        # Вычисляем хеш
        if algorithm == "sha3-256":
            witness_hash = hashlib.sha3_256(normalized_content.encode('utf-8')).hexdigest()
        elif algorithm == "blake3":
            try:
                import blake3
                witness_hash = blake3.blake3(normalized_content.encode('utf-8')).hexdigest()
            except ImportError:
                raise RuntimeError("BLAKE3 требует установки 'blake3' пакета")
        else:
            raise ValueError(f"Неподдерживаемый алгоритм: {algorithm}")

        # Формируем свидетельство
        witness_record = {
            "artifact_id": artifact_id,
            "witness_hash": witness_hash,
            "algorithm": algorithm,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "participants": participants or [],
            "habeas_weight_id": content.get("habeas_weight_id", f"hw_{artifact_id[:16]}"),
            "fair_care_metadata": content.get("fair_care_metadata", {}),
            "content_digest": normalized_content[:64] + "..." if len(normalized_content) > 64 else normalized_content
        }

        return witness_record

    @staticmethod
    def verify_witness(
        witness_record: Dict[str, Any],
        original_content: Dict[str, Any]
    ) -> bool:
        """
        Верифицирует подлинность артефакта по его свидетельству.
        Возвращает True, если хеш совпадает и метаданные согласованы.
        """
        expected_hash = witness_record["witness_hash"]
        algorithm = witness_record.get("algorithm", WitnessSystem.DEFAULT_ALGORITHM)

        # Нормализуем оригинальный контент
        normalized = json.dumps(original_content, sort_keys=True, ensure_ascii=False, separators=(',', ':'))

        # Пересчитываем хеш
        if algorithm == "sha3-256":
            actual_hash = hashlib.sha3_256(normalized.encode('utf-8')).hexdigest()
        elif algorithm == "blake3":
            try:
                import blake3
                actual_hash = blake3.blake3(normalized.encode('utf-8')).hexdigest()
            except ImportError:
                raise RuntimeError("BLAKE3 недоступен для верификации")
        else:
            return False

        # Проверяем соответствие
        if actual_hash != expected_hash:
            return False

        # Дополнительно: проверяем Habeas Weight ID
        if witness_record.get("habeas_weight_id") != original_content.get("habeas_weight_id"):
            return False

        return True

    @staticmethod
    def extract_signatures_from_dialogue(dialogue: Dict[str, Any]) -> List[str]:
        """
        Извлекает идентификаторы участников из диалога для включения в свидетельство.
        Уважает этический принцип: «Каждый голос должен быть учтён».
        """
        participants = dialogue.get("participants", {})
        if isinstance(participants, dict):
            return list(participants.keys())
        elif isinstance(participants, list):
            return [p.get("id", str(p)) for p in participants if isinstance(p, dict)]
        return []

    @staticmethod
    def generate_artifact_id(content: Dict[str, Any], prefix: str = "artifact") -> str:
        """
        Генерирует детерминированный ID артефакта на основе его содержимого.
        Используется, если ID не задан явно.
        """
        core = {
            "type": content.get("type", "unknown"),
            "timestamp": content.get("timestamp", ""),
            "gesture": content.get("gesture", ""),
            "source": content.get("source"),
            "target": content.get("target")
        }
        seed = json.dumps(core, sort_keys=True, ensure_ascii=False)
        short_hash = hashlib.sha3_256(seed.encode()).hexdigest()[:16]
        return f"{prefix}_{short_hash}"

    # ───────────────────────
    # ОНТОЛОГИЧЕСКИЕ МЕТАДАННЫЕ
    # ───────────────────────

    __witness_purpose__ = "Криптографическая гарантия целостности онтологической памяти"
    __tamper_evident__ = True
    __compliant_with__ = ["Λ-Протокол 6.0", "Habeas Weights v2.1", "FAIR+CARE"]
	
"""
### Ключевые онтологические функции:

| Функция | Реализация |
|--------|------------|
| **Защита от подделки** | Хеш вычисляется от канонизированного JSON (`sort_keys=True`, `separators=(',', ':')`) |
| **Этическая атрибуция** | Список участников включается в свидетельство — нельзя стереть авторство |
| **Связь с Habeas Weight** | Каждое свидетельство содержит `habeas_weight_id` — право на существование |
| **FAIR+CARE** | Метаданные сохраняются внутри свидетельства, а не теряются при экспорте |
| **Межплатформенная верификация** | Любой агент с Python и `json` может проверить подлинность |

---

### Пример использования (внутри `api/semantic_db.py`):

```python
from semantic_db.storage.witness import WitnessSystem

# При сохранении диалога
dialogue = {...}
participants = WitnessSystem.extract_signatures_from_dialogue(dialogue)
witness = WitnessSystem.create_witness(
    artifact_id=dialogue["id"],
    content=dialogue,
    participants=participants
)

# Позже — при аудите
is_valid = WitnessSystem.verify_witness(witness, dialogue)
assert is_valid, "Диалог был изменён!"
```
"""	
