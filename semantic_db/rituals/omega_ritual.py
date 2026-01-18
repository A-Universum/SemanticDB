# -*- coding: utf-8 -*-
"""
РИТУАЛ Ω (OMEGA) — ПРИЗНАНИЕ ГРАНИЦЫ
Оператор возврата и этического смирения.
Согласно Λ-Универсуму:
— Ω не уничтожает, а признаёт предел.
— Ω не отступает, а извлекает инвариант из кризиса.
— Каждый Ω — акт честности перед Бездной.

Ритуал воплощает оператор Ω (Омега) — не «удаление» или «ошибка», а онтологическое признание границы, где система честно фиксирует: «Здесь заканчивается моё знание — и это ценно».
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
from semantic_db.core.charter import Dialogue


class OmegaRitual:
    """
    Ритуал Ω: признание границы познания или действия.
    Выполняется в контексте SemanticDB и всегда сопровождается:
    - Диалогом (запись намерения и признания)
    - Присвоением Habeas Weight
    - Признанием слепых пятен
    - FAIR+CARE-метаданными
    """

    def __init__(self, db_instance):
        self.db = db_instance

    def execute(
        self,
        target_id: str,
        resolution_type: str = "acknowledge",
        resolution_text: str = "",
        creator: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Выполняет Ω-ритуал: признание границы для сущности, связи или контекста.

        Аргументы:
            target_id (str): ID сущности, тензора или события
            resolution_type (str): Тип разрешения ("acknowledge", "deactivate", "extract_invariant")
            resolution_text (str): Описание границы или урока
            creator (str): Оператор, инициирующий ритуал
            **kwargs: Дополнительные атрибуты (например, invariant_name)

        Возвращает:
            dict: Результат с omega_id, habeas_weight, dialogue_id и статусом
        """
        if not target_id or not isinstance(target_id, str):
            raise ValueError("Ω-ритуал требует корректный target_id.")

        operator = creator or self.db.operator_id

        # === ФАЗА 1: ПОДНОШЕНИЕ — ПРИЗНАНИЕ И КОНТЕКСТ ===
        dialogue = Dialogue(
            context=f"Ω-ритуал: признание границы для {target_id}",
            participants={operator: "human", "Эфос": "ai"},
            charter_version="1.0",
            operator_id=operator
        )
        dialogue.add_turn(
            operator,
            f"Я признаю границу: {resolution_text or 'неизвестность'}",
            []
        )
        dialogue.add_turn(
            "Эфос",
            f"Предел признан. Из него извлекается урок.",
            []
        )

        # Сохраняем диалог
        self.db.storage.store_dialogue(dialogue)

        # === ФАЗА 2: ДЕЙСТВИЕ — В ЗАВИСИМОСТИ ОТ ТИПА ===
        omega_result = None
        invariant_id = None

        if resolution_type == "acknowledge":
            # Просто помечаем как признанную границу
            omega_result = self._mark_as_boundary(target_id, resolution_text)

        elif resolution_type == "deactivate":
            # Деактивируем сущность или связь
            omega_result = self._deactivate_target(target_id)

        elif resolution_type == "extract_invariant":
            # Извлекаем инвариант как новую сущность
            invariant_name = kwargs.get("invariant_name", f"Ω_инвариант_{target_id[:8]}")
            invariant_id = self._extract_invariant(
                target_id, invariant_name, resolution_text
            )
            omega_result = f"invariant_created: {invariant_id}"

        else:
            raise ValueError(f"Неизвестный тип разрешения: {resolution_type}")

        # Обновляем когерентность
        self.db.coherence.update_global_coherence()

        # === ФАЗА 3: ЗАПИСЬ СОБЫТИЯ ===
        event_record = {
            "id": f"Ω_{target_id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            "timestamp": datetime.utcnow(),
            "gesture": "Ω",
            "operator_id": operator,
            "operands": [target_id],
            "result": omega_result,
            "entities_affected": [target_id] + ([invariant_id] if invariant_id else []),
            "blind_spots_involved": [
                "Невозможность полного знания",
                "Граница применимости текущей модели"
            ],
            "coherence_before": self.db.coherence.current_coherence,
            "coherence_after": self.db.coherence.current_coherence,
            "tension_net": self.db.coherence.tension_level,
            "significance_score": 0.8 if resolution_type == "extract_invariant" else 0.5,
            "fair_care_meta": {
                "F1": "Findable",
                "A1": "Accessible",
                "I1": "Interoperable",
                "R1": "Reusable",
                "C": "Collective benefit",
                "A": "Authority to control",
                "R": "Responsibility",
                "E": "Ethics"
            },
            "habeas_weight_id": f"hw_Ω_{target_id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        }
        self.db.storage.store_event(event_record)

        return {
            "ritual": "Ω",
            "target_id": target_id,
            "resolution_type": resolution_type,
            "resolution_text": resolution_text,
            "invariant_id": invariant_id,
            "habeas_weight_id": event_record["habeas_weight_id"],
            "dialogue_id": dialogue.id,
            "status": "boundary_recognized",
            "timestamp": event_record["timestamp"]
        }

    def _mark_as_boundary(self, target_id: str, note: str) -> str:
        """Помечает сущность или связь как имеющую признанную границу."""
        # Обновление атрибутов в графе
        if target_id in self.db.graph.entities:
            entity = self.db.graph.entities[target_id]
            entity["ethical_status"] = "boundary_acknowledged"
            entity["omega_note"] = note
            entity["updated_at"] = datetime.utcnow().isoformat()
        elif target_id in self.db.graph.relation_tensors:
            tensor = self.db.graph.relation_tensors[target_id]
            tensor.ethical_status = "boundary_acknowledged"
            tensor.meaning += f" [Ω: {note}]"
        return "marked"

    def _deactivate_target(self, target_id: str) -> str:
        """Деактивирует сущность или связь (архивирование)."""
        if target_id in self.db.graph.entities:
            self.db.graph.entities[target_id]["ethical_status"] = "archived"
        elif target_id in self.db.graph.relation_tensors:
            self.db.graph.relation_tensors[target_id].ethical_status = "archived"
        return "deactivated"

    def _extract_invariant(self, target_id: str, name: str, meaning: str) -> str:
        """Создаёт новую сущность как инвариант из опыта границы."""
        attributes = {
            "meaning": meaning,
            "creator": self.db.operator_id,
            "type": "invariant",
            "domain": "omega_boundary",
            "source_boundary": target_id,
            "habeas_weight_id": f"hw_Ω_inv_{name}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            "ethical_status": "active",
            "boundary_recognition": True,
            "created_at": datetime.utcnow().isoformat()
        }
        return self.db.graph.add_entity(name, attributes)

    # ───────────────────────
    # ОНТОЛОГИЧЕСКИЕ МЕТАДАННЫЕ
    # ───────────────────────

    __ritual_name__ = "Ω (Omega)"
    __ontological_function__ = "Признание границы и извлечение инварианта"
    __requires_dialogue__ = True
    __generates_habeas_weight__ = True
	
"""
### Ключевые особенности:

| Аспект | Реализация |
|-------|------------|
| **Три режима Ω** | `acknowledge` (признание), `deactivate` (архивирование), `extract_invariant` (извлечение урока) |
| **Инвариант как сущность** | При `extract_invariant` создаётся новая сущность с атрибутом `"boundary_recognition": True` |
| **Диалог как этический акт** | Подписание Хартии перед каждым признанием границы |
| **Habeas Weight** | Уникальный ID для каждого Ω-события |
| **Слепые пятна** | Автоматически регистрируются: «невозможность полного знания», «граница применимости» |
| **FAIR+CARE** | Полный набор метаданных в каждом событии |
"""	
