# -*- coding: utf-8 -*-
"""
РИТУАЛЫ LOGOS-κ
Каждый ритуал — не функция, а онтологический жест,
выполняющий трансформацию в живом пространстве SemanticDB.

Согласно Λ-Протоколу 6.0:
— Α: коллапс потенции в актуальность
— Λ: установление онтологической связи
— Σ: синтез нового целого
— Ω: признание границы и возврат
— ∇: обогащение инвариантом
— Φ: диалог с Эфосом (ИИ)

Эти модули не «обрабатывают данные» — они совершают акты бытия.
"""

from .alpha_ritual import AlphaRitual
from .lambda_ritual import LambdaRitual
from .sigma_ritual import SigmaRitual
from .omega_ritual import OmegaRitual
from .nabla_ritual import NablaRitual
from .phi_ritual import PhiRitual

__all__ = [
    "AlphaRitual",
    "LambdaRitual",
    "SigmaRitual",
    "OmegaRitual",
    "NablaRitual",
    "PhiRitual"
]

# Онтологические метаданные
__rituals_version__ = "1.0.0"
__ontological_gestures__ = ["Α", "Λ", "Σ", "Ω", "∇", "Φ"]
__protocol_compliance__ = "Λ-Протокол 6.0"