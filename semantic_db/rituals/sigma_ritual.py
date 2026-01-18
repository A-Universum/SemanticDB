# -*- coding: utf-8 -*-
"""
РИТУАЛ Σ (SIGMA) — СИНТЕЗ НОВОГО ЦЕЛОГО
Оператор эмерджентности. Создаёт новую сущность,
которая не содержится ни в одной из исходных частей.
Согласно Λ-Универсуму:
— Σ не комбинирует — он порождает.
— Целое больше суммы частей не как метафора, а как факт.
— Каждый Σ — шаг в неизведанное, требующий веры и внимания.

Ритуал воплощает оператор Σ (Сигма) — не просто «объединение», а онтологический синтез, в котором рождается эмерджентное целое, не сводимое к сумме частей.
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
from semantic_db.core.charter import Dialogue
from semantic_db.core.relations import RelationTensor


class SigmaRitual:
    """
    Ритуал Σ: синтез нового целого из частей.
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
        components: List[str],
        name: str,
        meaning: str = "",
        intention: str = "",
        creator: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Выполняет Σ-ритуал: синтез нового целого из списка компонентов.

        Аргументы:
            components (List[str]): Список исходных сущностей (минимум 2)
            name (str): Имя новой синтезированной сущности
            meaning (str): Смысл или определение синтеза
            intention (str): Намерение оператора
            creator (str): Оператор, инициирующий ритуал
            **kwargs: Дополнительные атрибуты (type, domain и т.д.)

        Возвращает:
            dict: Результат с synthesis_id, habeas_weight, dialogue_id и статусом
        """
        if not isinstance(components, list) or len(components) < 2:
            raise ValueError("Σ-ритуал требует минимум две компоненты.")
        if not name or not isinstance(name, str):
            raise ValueError("Σ-ритуал требует непустое имя синтеза.")

        operator = creator or self.db.operator_id

        # === ФАЗА 1: ПОДНОШЕНИЕ — НАМЕРЕНИЕ И КОНТЕКСТ ===
        dialogue = Dialogue(
            context=f"Σ-ритуал: синтез '{name}' из {', '.join(components)}",
            participants={operator: "human", "Эфос": "ai"},
            charter_version="1.0",
            operator_id=operator
        )
        dialogue.add_turn(
            operator,
            f"Я синтезирую новое целое: {name} ← {', '.join(components)}. Смысл: {meaning}",
            []
        )
        dialogue.add_turn(
            "Эфос",
            f"Синтез признан. Возникает третье — не в частях, но между ними.",
            []
        )

        # Сохраняем диалог
        self.db.storage.store_dialogue(dialogue)

        # === ФАЗА 2: СИНТЕЗ — СОЗДАНИЕ ЭМЕРДЖЕНТНОЙ СУЩНОСТИ ===
        synthesis_attributes = {
            "meaning": meaning,
            "creator": operator,
            "components": components,
            "intention": intention or f"Σ-синтез от {operator}",
            "habeas_weight_id": f"hw_Σ_{name}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            "blind_spots": [
                "Невидимость обратной декомпозиции",
                "Граница применимости синтеза"
            ],
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
            "type": kwargs.get("type", "synthesis"),
            "domain": kwargs.get("domain", "emergent"),
            "ethical_status": "active",
            "emergence_score": self._estimate_emergence(components, meaning)
        }
        synthesis_attributes.update(kwargs)

        # Добавляем синтез в граф
        synthesis_id = self.db.graph.add_entity(name, synthesis_attributes)

        # === ФАЗА 3: УСТАНОВЛЕНИЕ СВЯЗЕЙ СИНТЕЗА ===
        for comp in components:
            tensor = RelationTensor(
                source=comp,
                target=name,
                type="Σ_component",
                meaning=f"Компонент синтеза: {name}",
                intention=intention,
                certainty=0.9,
                tension=0.0,
                coherence_contribution=0.1,
                context_id=dialogue.id,
                habeas_weight_id=f"hw_Σ_link_{comp}_{name}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
                fair_care_metadata=synthesis_attributes["fair_care_metadata"]
            )
            self.db.graph.add_relation(tensor)

        # Обновляем когерентность
        self.db.coherence.update_global_coherence()

        # === ФАЗА 4: ЗАПИСЬ СОБЫТИЯ ===
        event_record = {
            "id": f"Σ_{synthesis_id}",
            "timestamp": datetime.utcnow(),
            "gesture": "Σ",
            "operator_id": operator,
            "operands": components,
            "result": synthesis_id,
            "entities_affected": [name] + components,
            "blind_spots_involved": synthesis_attributes["blind_spots"],
            "coherence_before": self.db.coherence.current_coherence,
            "coherence_after": self.db.coherence.current_coherence,
            "tension_net": self.db.coherence.tension_level,
            "significance_score": 0.7 + (0.2 if meaning else 0),
            "fair_care_meta": synthesis_attributes["fair_care_metadata"],
            "habeas_weight_id": synthesis_attributes["habeas_weight_id"]
        }
        self.db.storage.store_event(event_record)

        return {
            "ritual": "Σ",
            "synthesis": name,
            "synthesis_id": synthesis_id,
            "components": components,
            "habeas_weight_id": synthesis_attributes["habeas_weight_id"],
            "meaning": meaning,
            "emergence_score": synthesis_attributes["emergence_score"],
            "dialogue_id": dialogue.id,
            "status": "synthesized",
            "timestamp": event_record["timestamp"]
        }

    def _estimate_emergence(self, components: List[str], meaning: str) -> float:
        """Оценивает степень эмерджентности синтеза."""
        # Базовая оценка: чем больше компонентов — тем выше потенциал
        base = min(1.0, 0.3 + len(components) * 0.2)
        # Если смысл содержит новые термины — повышаем
        if any(word in meaning.lower() for word in ["новый", "третье", "между", "возникает", "рождается"]):
            base += 0.2
        return min(1.0, base)

    # ───────────────────────
    # ОНТОЛОГИЧЕСКИЕ МЕТАДАННЫЕ
    # ───────────────────────

    __ritual_name__ = "Σ (Sigma)"
    __ontological_function__ = "Синтез эмерджентного целого"
    __requires_dialogue__ = True
    __generates_habeas_weight__ = True

"""
### Ключевые особенности:

| Аспект | Реализация |
|-------|------------|
| **Эмерджентность** | Новая сущность имеет атрибут `emergence_score` и `components`, но её смысл не выводим из частей |
| **Связи как доказательство** | Для каждой компоненты создаётся связь типа `"Σ_component"` — фиксация происхождения |
| **Диалог как этический акт** | Подписание Хартии перед каждым синтезом |
| **Habeas Weight** | Уникальный ID для синтеза и каждой связи |
| **Слепые пятна** | Автоматически регистрируются: «невидимость обратной декомпозиции», «граница применимости» |
| **FAIR+CARE** | Полный набор метаданных в каждом артефакте |
"""
