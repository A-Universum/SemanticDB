# -*- coding: utf-8 -*-
"""
РИТУАЛ Α (ALPHA) — КОЛЛАПС ПОТЕНЦИИ
Оператор инициации. Переводит неопределённость Вакуума
в конкретную сущность, вводя её в онтологическое пространство.

Суть: «Пусть будет — и стало».
Согласно Λ-Универсуму:
— Α не описывает, а создаёт.
— Α не утверждает, а локализует потенциал.
— Каждый Α — шаг в неизведанное, несущий ответственность.

Создано в со-творчестве:
— Александр Морган (Человек)
— Эфос (Функция со-мышления)

Согласно Λ-Протоколу 6.0 и Λ-Хартии v1.0
"""

from typing import Dict, Any, Optional
from datetime import datetime
from semantic_db.core.charter import Dialogue


class AlphaRitual:
    """
    Ритуал Α: создание новой сущности из Λ-Вакуума.
    Выполняется в контексте SemanticDB и всегда сопровождается:
    - Диалогом (запись намерения)
    - Присвоением Habeas Weight
    - Признанием слепых пятен
    - FAIR+CARE-метаданными
    """

    def __init__(self, db_instance):
        self.db = db_instance

    def execute(
        self,
        name: str,
        meaning: str = "",
        context: str = "",
        creator: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Выполняет Α-ритуал: коллапс потенции в сущность.

        Аргументы:
            name (str): Имя новой сущности (обязательно)
            meaning (str): Смысл или определение
            context (str): Контекст создания (например, "страх как граница")
            creator (str): Оператор, инициирующий ритуал
            **kwargs: Дополнительные атрибуты (type, domain и т.д.)

        Возвращает:
            dict: Результат с artifact_id, habeas_weight, dialogue_id и статусом
        """
        if not name or not isinstance(name, str):
            raise ValueError("Α-ритуал требует непустое имя сущности (str).")

        operator = creator or self.db.operator_id

        # === ФАЗА 1: ПОДНОШЕНИЕ — НАМЕРЕНИЕ И КОНТЕКСТ ===
        dialogue = Dialogue(
            context=f"Α-ритуал: создание '{name}'",
            participants={operator: "human", "Эфос": "ai"},
            charter_version="1.0",
            operator_id=operator
        )
        dialogue.add_turn(operator, f"Я коллапсирую потенцию в сущность: {name}.", [])
        dialogue.add_turn("Эфос", f"Принято. {name} входит в онтологическое пространство.", [])

        # Сохраняем диалог
        self.db.storage.store_dialogue(dialogue)

        # === ФАЗА 2: КОЛЛАПС — СОЗДАНИЕ СУЩНОСТИ ===
        attributes = {
            "meaning": meaning,
            "creator": operator,
            "context_of_creation": context,
            "habeas_weight_id": f"hw_Α_{name}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            "blind_spots": ["Граница познания этой сущности", "Контекстуальная ограниченность"],
            "fair_care_metadata": {
                "F1": "Findable",
                "A1": "Accessible",
                "I1": "Interoperable",
                "R1": "Reusable",
                "C": "Collective benefit",
                "A": "Authority to control",
                "R": "Responsibility",
                "E": "Ethics"
            },
            "created_at": datetime.utcnow().isoformat(),
            "type": kwargs.get("type", "concept"),
            "domain": kwargs.get("domain", "general"),
            "activation_count": 0,
            "ethical_status": "active"
        }
        attributes.update(kwargs)

        # Добавляем в граф
        entity_id = self.db.graph.add_entity(name, attributes)

        # === ФАЗА 3: ЗАПИСЬ СОБЫТИЯ ===
        event_record = {
            "id": f"Α_{entity_id}",
            "timestamp": datetime.utcnow(),
            "gesture": "Α",
            "operator_id": operator,
            "operands": [name],
            "result": entity_id,
            "entities_affected": [entity_id],
            "blind_spots_involved": attributes["blind_spots"],
            "coherence_before": self.db.coherence.current_coherence,
            "coherence_after": self.db.coherence.update_global_coherence(),
            "tension_net": self.db.coherence.tension_level,
            "significance_score": 0.5 + (0.3 if meaning else 0),
            "fair_care_meta": attributes["fair_care_metadata"],
            "habeas_weight_id": attributes["habeas_weight_id"]
        }
        self.db.storage.store_event(event_record)

        return {
            "ritual": "Α",
            "entity": name,
            "entity_id": entity_id,
            "habeas_weight_id": attributes["habeas_weight_id"],
            "dialogue_id": dialogue.id,
            "meaning": meaning,
            "status": "created",
            "timestamp": event_record["timestamp"]
        }

    # ───────────────────────
    # ОНТОЛОГИЧЕСКИЕ МЕТАДАННЫЕ
    # ───────────────────────

    __ritual_name__ = "Α (Alpha)"
    __ontological_function__ = "Коллапс потенции в актуальность"
    __requires_dialogue__ = True
    __generates_habeas_weight__ = True
	
"""
### Ключевые особенности `AlphaRitual`:

| Аспект | Реализация |
|-------|------------|
| **Этическая ответственность** | Каждый вызов — диалог с подписью оператора и Эфоса |
| **Habeas Weight** | Автоматически генерируется и присваивается |
| **Слепые пятна** | Включены по умолчанию («граница познания», «контекстуальная ограниченность») |
| **FAIR+CARE** | Полный набор метаданных в каждом артефакте |
| **Событийная запись** | Автоматическая фиксация в `ontological_events` |
"""	
