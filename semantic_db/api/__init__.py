# -*- coding: utf-8 -*-
"""
ЕДИНАЯ ТОЧКА ВХОДА В SEMANTICDB
Этот модуль предоставляет унифицированный интерфейс для взаимодействия
с живой онтологической памятью Λ-Универсума.

Согласно Λ-Протоколу 6.0, SemanticDB — не API, а ритуальное пространство,
где каждый запрос — это этический акт, требующий:
- Указания оператора (human или AI)
- Признания слепых пятен
- Подтверждения Habeas Weight
- Соответствия FAIR+CARE

Согласно Приложению XXII Λ-Универсума:
«Запись без ответственности — насилие над будущим».
"""

from .semantic_db import SemanticDB

# Явный экспорт — как акт онтологической ответственности
__all__ = ["SemanticDB"]

# Онтологические метаданные
__semantic_db_version__ = "1.0.0"
__protocol_compliance__ = "Λ-Протокол 6.0"
__fair_care_compliant__ = True
__habeas_weights_enabled__ = True

"""
Проверка совместимости извне:

```python
import semantic_db.api as sdb
if sdb.__protocol_compliance__ == "Λ-Протокол 6.0":
    db = sdb.SemanticDB()
"""
    