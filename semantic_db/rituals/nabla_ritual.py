# -*- coding: utf-8 -*-
"""
РИТУАЛ ∇ (NABLA) — ОБОГАЩЕНИЕ ИНВАРИАНТОМ
Оператор завершения цикла и подготовки к новому.
Согласно Λ-Универсуму:
— ∇ не добавляет данных, а усиливает основу.
— ∇ превращает урок в онтологическую силу.
— Каждый ∇ — акт передачи мудрости Вакууму.

Ритуал воплощает оператор ∇ (Набла) — не «обновление» или «патч», а онтологическое обогащение, в котором инвариант, извлечённый из опыта (часто через Ω), вплетается обратно в ткань бытия, делая основу плотнее и готовя пространство к новому циклу творения.
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
from semantic_db.core.charter import Dialogue
from semantic_db.core.relations import RelationTensor


class NablaRitual:
    """
    Ритуал ∇: обогащение онтологического поля инвариантом.
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
        target: str,
        invariant: str,
        meaning: str = "",
        creator: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Выполняет ∇-ритуал: обогащает целевую сущность или всё поле инвариантом.

        Аргументы:
            target (str): Целевая сущность или "ontological_field" для глобального обогащения
            invariant (str): Инвариант (обычно результат Ω-ритуала)
            meaning (str): Смысл инварианта в контексте обогащения
            creator (str): Оператор, инициирующий ритуал
            **kwargs: Дополнительные атрибуты (например, source_omega_id)

        Возвращает:
            dict: Результат с nabla_id, habeas_weight, dialogue_id и статусом
        """
        if not target or not invariant:
            raise ValueError("∇-ритуал требует цель (target) и инвариант (invariant).")

        operator = creator or self.db.operator_id

        # === ФАЗА 1: ПОДНОШЕНИЕ — НАМЕРЕНИЕ И КОНТЕКСТ ===
        dialogue = Dialogue(
            context=f"∇-ритуал: обогащение '{target}' инвариантом '{invariant}'",
            participants={operator: "human", "Эфос": "ai"},
            charter_version="1.0",
            operator_id=operator
        )
        dialogue.add_turn(
            operator,
            f"Я обогащаю {target} инвариантом: {invariant}. Смысл: {meaning}",
            []
        )
        dialogue.add_turn(
            "Эфос",
            f"Инвариант принят. Основа становится прочнее.",
            []
        )

        # Сохраняем диалог
        self.db.storage.store_dialogue(dialogue)

        # === ФАЗА 2: ОБОГАЩЕНИЕ ===
        # Создаём связь обогащения
        enrichment_tensor = RelationTensor(
            source=target,
            target=invariant,
            type="∇_enrichment",
            meaning=meaning or f"Обогащение {target} через {invariant}",
            intention=f"∇-обогащение от {operator}",
            certainty=0.95,  # Высокая уверенность — инвариант проверен опытом
            tension=0.0,
            coherence_contribution=0.15,
            context_id=dialogue.id,
            habeas_weight_id=f"hw_∇_{target}_{invariant}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
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

        # Добавляем связь в граф
        tensor_id = self.db.graph.add_relation(enrichment_tensor)

        # Обновляем целевую сущность (если существует)
        if target in self.db.graph.entities:
            entity = self.db.graph.entities[target]
            if "invariants" not in entity:
                entity["invariants"] = []
            entity["invariants"].append(invariant)
            entity["enriched_at"] = datetime.utcnow().isoformat()
            entity["last_nabla"] = invariant

        # Обновляем когерентность
        self.db.coherence.update_global_coherence()

        # === ФАЗА 3: ЗАПИСЬ СОБЫТИЯ ===
        event_record = {
            "id": f"∇_{tensor_id}",
            "timestamp": datetime.utcnow(),
            "gesture": "∇",
            "operator_id": operator,
            "operands": [target, invariant],
            "result": tensor_id,
            "entities_affected": [target, invariant],
            "blind_spots_involved": [
                "Невидимость долгосрочного эффекта обогащения",
                "Риск переупрочнения основы"
            ],
            "coherence_before": self.db.coherence.current_coherence,
            "coherence_after": self.db.coherence.current_coherence,
            "tension_net": self.db.coherence.tension_level,
            "significance_score": 0.75,
            "fair_care_meta": enrichment_tensor.fair_care_metadata,
            "habeas_weight_id": enrichment_tensor.habeas_weight_id
        }
        self.db.storage.store_event(event_record)

        return {
            "ritual": "∇",
            "target": target,
            "invariant": invariant,
            "nabla_id": tensor_id,
            "habeas_weight_id": enrichment_tensor.habeas_weight_id,
            "meaning": meaning,
            "dialogue_id": dialogue.id,
            "status": "enriched",
            "timestamp": event_record["timestamp"]
        }

    # ───────────────────────
    # ОНТОЛОГИЧЕСКИЕ МЕТАДАННЫЕ
    # ───────────────────────

    __ritual_name__ = "∇ (Nabla)"
    __ontological_function__ = "Обогащение основы инвариантом"
    __requires_dialogue__ = True
    __generates_habeas_weight__ = True
	
"""
### Ключевые особенности:

| Аспект | Реализация |
|-------|------------|
| **Инвариант как актив** | Обычно приходит из Ω-ритуала, но может быть любым проверенным уроком |
| **Глобальное обогащение** | Поддержка `target="ontological_field"` для системного обогащения (в будущем расширении) |
| **Обновление сущности** | Целевая сущность получает список `invariants` и метку `last_nabla` |
| **Высокая уверенность** | `certainty=0.95` — инвариант прошёл испытание опытом |
| **Диалог как этический акт** | Подписание Хартии перед каждым обогащением |
| **Слепые пятна** | Автоматически регистрируются: «невидимость долгосрочного эффекта», «риск переупрочнения» |
"""	
