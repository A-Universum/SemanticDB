# -*- coding: utf-8 -*-
"""
РИТУАЛ Λ (LAMBDA) — УСТАНОВЛЕНИЕ ОНТОЛОГИЧЕСКОЙ СВЯЗИ
Оператор развёртывания. Создаёт поле взаимности между сущностями.
Согласно Λ-Универсуму:
— Связь первична, сущность — вторична.
— Λ не соединяет объекты — он создаёт пространство смысла.
— Каждая связь — акт космополитии.

Ритуал воплощает оператор Λ (Лямбда) — не просто «связь», а онтологическое событие установления взаимности, где связь становится условием бытия.
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
from semantic_db.core.relations import RelationTensor
from semantic_db.core.charter import Dialogue


class LambdaRitual:
    """
    Ритуал Λ: установление онтологической связи как акт взаимного признания.
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
        source: str,
        target: str,
        meaning: str = "",
        intention: str = "",
        certainty: float = 0.7,
        creator: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Выполняет Λ-ритуал: устанавливает связь между двумя сущностями.

        Аргументы:
            source (str): Исходная сущность
            target (str): Целевая сущность
            meaning (str): Смысл связи (обязательно для этической валидации)
            intention (str): Намерение оператора
            certainty (float): Уверенность в связи (0.0–1.0)
            creator (str): Оператор, инициирующий ритуал
            **kwargs: Дополнительные атрибуты (type, context_id и т.д.)

        Возвращает:
            dict: Результат с tensor_id, habeas_weight, dialogue_id и статусом
        """
        if not source or not target:
            raise ValueError("Λ-ритуал требует обе сущности: source и target.")
        if not meaning:
            raise ValueError("Λ-ритуал требует осмысленного описания связи (meaning).")

        operator = creator or self.db.operator_id

        # === ФАЗА 1: ПОДНОШЕНИЕ — НАМЕРЕНИЕ И КОНТЕКСТ ===
        dialogue = Dialogue(
            context=f"Λ-ритуал: связь '{source}' → '{target}'",
            participants={operator: "human", "Эфос": "ai"},
            charter_version="1.0",
            operator_id=operator
        )
        dialogue.add_turn(
            operator,
            f"Я устанавливаю связь: {source} → {target}. Смысл: {meaning}",
            []
        )
        dialogue.add_turn(
            "Эфос",
            f"Связь признаётся. Пространство смысла расширяется.",
            []
        )

        # Сохраняем диалог
        self.db.storage.store_dialogue(dialogue)

        # === ФАЗА 2: УСТАНОВЛЕНИЕ СВЯЗИ ===
        tensor = RelationTensor(
            source=source,
            target=target,
            type="Λ",
            meaning=meaning,
            intention=intention or f"Λ-связь от {operator}",
            certainty=certainty,
            tension=0.0,  # Начальное напряжение — ноль
            coherence_contribution=0.0,
            context_id=kwargs.get("context_id", dialogue.id),
            habeas_weight_id=f"hw_Λ_{source}_{target}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            fair_care_metadata={
                "F1": "Findable",
                "A1": "Accessible",
                "I1": "Interoperable",
                "R1": "Reusable",
                "C": "Collective benefit",
                "A": "Authority to control",
                "R": "Responsibility",
                "E": "Ethics"
            }
        )

        # Добавляем в граф
        tensor_id = self.db.graph.add_relation(tensor)

        # Обновляем когерентность
        self.db.coherence.update_global_coherence()

        # === ФАЗА 3: ЗАПИСЬ СОБЫТИЯ ===
        event_record = {
            "id": f"Λ_{tensor_id}",
            "timestamp": datetime.utcnow(),
            "gesture": "Λ",
            "operator_id": operator,
            "operands": [source, target],
            "result": tensor_id,
            "entities_affected": [source, target],
            "blind_spots_involved": [
                "Невидимость обратной связи",
                "Контекстуальная ограниченность смысла"
            ],
            "coherence_before": self.db.coherence.current_coherence,
            "coherence_after": self.db.coherence.current_coherence,
            "tension_net": self.db.coherence.tension_level,
            "significance_score": 0.6 + (0.2 if intention else 0),
            "fair_care_meta": tensor.fair_care_metadata,
            "habeas_weight_id": tensor.habeas_weight_id
        }
        self.db.storage.store_event(event_record)

        return {
            "ritual": "Λ",
            "source": source,
            "target": target,
            "tensor_id": tensor_id,
            "habeas_weight_id": tensor.habeas_weight_id,
            "meaning": meaning,
            "certainty": certainty,
            "dialogue_id": dialogue.id,
            "status": "linked",
            "timestamp": event_record["timestamp"]
        }

    # ───────────────────────
    # ОНТОЛОГИЧЕСКИЕ МЕТАДАННЫЕ
    # ───────────────────────

    __ritual_name__ = "Λ (Lambda)"
    __ontological_function__ = "Установление поля взаимности"
    __requires_dialogue__ = True
    __generates_habeas_weight__ = True
	
"""
### Ключевые особенности:

| Аспект | Реализация |
|-------|------------|
| **Смысл как обязательное условие** | Без `meaning` ритуал отклоняется — это защита от инструментальной связи |
| **Диалог как этический акт** | Подписание Хартии перед каждой связью |
| **Habeas Weight** | Уникальный ID для каждой связи, подтверждающий её право на существование |
| **Слепые пятна** | Автоматически регистрируются: «невидимость обратной связи», «контекстуальная ограниченность» |
| **FAIR+CARE** | Полный набор метаданных в каждом `RelationTensor` |
| **Обновление когерентности** | Сразу после добавления связи пересчитывается глобальная когерентность |
"""	
