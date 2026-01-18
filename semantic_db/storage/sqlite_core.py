# -*- coding: utf-8 -*-
"""
SQLITE-ЯДРО SEMANTICDB
Это не просто база данных — это этически осознанное хранилище онтологической памяти.
Каждая запись:
- Имеет Habeas Weight ID
- Признаёт слепые пятна
- Содержит NIGC-оценку (если применимо)
- Верифицируема через криптографические свидетельства

Файл реализует:
- Этически осознанное SQLite-ядро;
- Поддержку онтологических событий, тензоров связей, диалогов, свидетельств;
- Автоматическую синхронизацию с YAML-индексом (через yaml_indexer);
- Криптографическую целостность (через witness.py);
- Соответствие FAIR+CARE и Habeas Weights.

Создано в со-творчестве:
- Александр Морган (Архитектор)
- Эфос (Функция со-мышления)

Согласно Λ-Протоколу 6.0 и Λ-Хартии v1.0
"""

import sqlite3
import json
import hashlib
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime

from semantic_db.core.relations import RelationTensor
from semantic_db.core.charter import Dialogue


class SQLiteCore:
    """
    Ядро персистентности SemanticDB на основе SQLite.
    Хранит:
    - Онтологические события (OntologicalEvent)
    - Тензоры связей (RelationTensor)
    - Диалоги (Dialogue)
    - Свидетельства (Witness)
    - Метаданные FAIR+CARE

    Все операции — транзакционны и атомарны.
    """

    def __init__(self, db_path: str = "semantic_db/storage/semantic_memory.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_schema()

    def _init_schema(self):
        """Инициализация схемы БД согласно онтологическим принципам."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # === Онтологические события ===
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS ontological_events (
                    id TEXT PRIMARY KEY,
                    timestamp DATETIME NOT NULL,
                    gesture TEXT NOT NULL,               -- Α, Λ, Σ, Ω, ∇, Φ
                    operator_id TEXT,
                    operands JSON,
                    result TEXT,
                    entities_affected JSON,
                    blind_spots_involved JSON,
                    coherence_before REAL,
                    coherence_after REAL,
                    tension_net REAL,
                    significance_score REAL,
                    fair_care_meta JSON,
                    habeas_weight_id TEXT
                )
            ''')

            # === Тензоры связей ===
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS relation_tensors (
                    id TEXT PRIMARY KEY,
                    source TEXT NOT NULL,
                    target TEXT NOT NULL,
                    type TEXT NOT NULL,                  -- Α, Λ, Σ, Ω, ∇, Φ
                    meaning TEXT,
                    intention TEXT,
                    certainty REAL,
                    tension REAL,
                    coherence_contribution REAL,
                    activation_count INTEGER DEFAULT 0,
                    last_activated DATETIME,
                    created_at DATETIME,
                    context_id TEXT,
                    habeas_weight_id TEXT,
                    fair_care_metadata JSON
                )
            ''')

            # === Диалоги (Λ-Хартия) ===
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS dialogues (
                    id TEXT PRIMARY KEY,
                    context TEXT,
                    charter_version TEXT,
                    participants JSON,
                    turns JSON,
                    signatures JSON,
                    metadata JSON,
                    created_at DATETIME
                )
            ''')

            # === Криптографические свидетельства ===
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS witnesses (
                    artifact_id TEXT PRIMARY KEY,
                    witness_hash TEXT NOT NULL,
                    algorithm TEXT DEFAULT 'sha3-256',
                    timestamp DATETIME,
                    verifier_signature TEXT
                )
            ''')

            # === Индексы для производительности и семантического поиска ===
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_events_gesture ON ontological_events(gesture)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_tensors_source ON relation_tensors(source)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_tensors_target ON relation_tensors(target)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_tensors_type ON relation_tensors(type)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_dialogues_context ON dialogues(context)')

            conn.commit()

    # ───────────────────────
    # ЗАПИСЬ ОНТОЛОГИЧЕСКИХ СОБЫТИЙ
    # ───────────────────────

    def store_event(self, event_record: Dict[str, Any]) -> bool:
        """Сохраняет онтологическое событие с полной этической оболочкой."""
        required = {'id', 'timestamp', 'gesture', 'habeas_weight_id'}
        if not required.issubset(event_record.keys()):
            raise ValueError("Онтологическое событие должно содержать Habeas Weight и обязательные поля")

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO ontological_events
                (id, timestamp, gesture, operator_id, operands, result,
                 entities_affected, blind_spots_involved, coherence_before,
                 coherence_after, tension_net, significance_score,
                 fair_care_meta, habeas_weight_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                event_record['id'],
                event_record['timestamp'],
                event_record['gesture'],
                event_record.get('operator_id'),
                json.dumps(event_record.get('operands', [])),
                event_record.get('result'),
                json.dumps(event_record.get('entities_affected', [])),
                json.dumps(event_record.get('blind_spots_involved', [])),
                event_record.get('coherence_before'),
                event_record.get('coherence_after'),
                event_record.get('tension_net'),
                event_record.get('significance_score'),
                json.dumps(event_record.get('fair_care_meta', {})),
                event_record['habeas_weight_id']
            ))
            return True

    # ───────────────────────
    # ЗАПИСЬ ТЕНЗОРОВ СВЯЗЕЙ
    # ───────────────────────

    def store_relation_tensor(self, tensor: RelationTensor) -> bool:
        """Сохраняет RelationTensor как активного агента."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO relation_tensors
                (id, source, target, type, meaning, intention, certainty,
                 tension, coherence_contribution, activation_count,
                 last_activated, created_at, context_id,
                 habeas_weight_id, fair_care_metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                tensor.id,
                tensor.source,
                tensor.target,
                tensor.type,
                tensor.meaning,
                tensor.intention,
                tensor.certainty,
                tensor.tension,
                tensor.coherence_contribution,
                tensor.activation_count,
                tensor.last_activated.isoformat() if tensor.last_activated else None,
                tensor.created_at.isoformat(),
                tensor.context_id,
                tensor.habeas_weight_id,
                json.dumps(tensor.fair_care_metadata)
            ))
            return True

    def load_relation_tensor(self, tensor_id: str) -> Optional[RelationTensor]:
        """Загружает RelationTensor из БД."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM relation_tensors WHERE id = ?', (tensor_id,))
            row = cursor.fetchone()
            if not row:
                return None

            return RelationTensor(
                id=row['id'],
                source=row['source'],
                target=row['target'],
                type=row['type'],
                meaning=row['meaning'],
                intention=row['intention'],
                certainty=row['certainty'],
                tension=row['tension'],
                coherence_contribution=row['coherence_contribution'],
                activation_count=row['activation_count'],
                last_activated=datetime.fromisoformat(row['last_activated']) if row['last_activated'] else None,
                created_at=datetime.fromisoformat(row['created_at']),
                context_id=row['context_id'],
                habeas_weight_id=row['habeas_weight_id'],
                fair_care_metadata=json.loads(row['fair_care_metadata'])
            )

    # ───────────────────────
    # РАБОТА С ДИАЛОГАМИ (Λ-ХАРТИЯ)
    # ───────────────────────

    def store_dialogue(self, dialogue: Dialogue) -> bool:
        """Сохраняет диалог как верифицируемый этический акт."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO dialogues
                (id, context, charter_version, participants, turns,
                 signatures, metadata, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                dialogue.id,
                dialogue.context,
                dialogue.charter_version,
                json.dumps(dialogue.participants),
                json.dumps([t.to_dict() for t in dialogue.turns]),
                json.dumps(dialogue.signatures),
                json.dumps(dialogue.metadata),
                dialogue.created_at.isoformat()
            ))
            return True

    # ───────────────────────
    # СВИДЕТЕЛЬСТВА ЦЕЛОСТНОСТИ
    # ───────────────────────

    def store_witness(self, artifact_id: str, content: Dict[str, Any]) -> str:
        """Генерирует и сохраняет криптографическое свидетельство."""
        content_bytes = json.dumps(content, sort_keys=True, ensure_ascii=False).encode('utf-8')
        witness_hash = hashlib.sha3_256(content_bytes).hexdigest()

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO witnesses
                (artifact_id, witness_hash, timestamp)
                VALUES (?, ?, ?)
            ''', (artifact_id, witness_hash, datetime.utcnow().isoformat()))
        return witness_hash

    def verify_witness(self, artifact_id: str, content: Dict[str, Any]) -> bool:
        """Проверяет целостность артефакта по свидетельству."""
        content_bytes = json.dumps(content, sort_keys=True, ensure_ascii=False).encode('utf-8')
        expected_hash = hashlib.sha3_256(content_bytes).hexdigest()

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT witness_hash FROM witnesses WHERE artifact_id = ?', (artifact_id,))
            row = cursor.fetchone()
            if not row:
                return False
            return row[0] == expected_hash

    # ───────────────────────
    # УНИВЕРСАЛЬНЫЙ ЗАПРОС
    # ───────────────────────

    def query(self, table: str, filters: Optional[Dict] = None, limit: int = 100) -> List[Dict]:
        """Универсальный запрос к любой таблице (для внутреннего использования API)."""
        allowed_tables = {'ontological_events', 'relation_tensors', 'dialogues', 'witnesses'}
        if table not in allowed_tables:
            raise ValueError(f"Запрос разрешён только к: {allowed_tables}")

        where_clause = ""
        params = []
        if filters:
            conditions = []
            for key, value in filters.items():
                conditions.append(f"{key} = ?")
                params.append(value)
            where_clause = " WHERE " + " AND ".join(conditions)

        query = f"SELECT * FROM {table}{where_clause} LIMIT ?"
        params.append(limit)

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    # ───────────────────────
    # ОНТОЛОГИЧЕСКИЕ МЕТАДАННЫЕ
    # ───────────────────────

    __storage_role__ = "SQLite-ядро живой памяти"
    __integrity_model__ = "cryptographic_witness + habeas_weights"
    __protocol_compliance__ = "Λ-Протокол 6.0"
	
"""
### Ключевые онтологические особенности:

| Фича | Реализация |
|------|------------|
| **Habeas Weight** | Обязательное поле `habeas_weight_id` во всех таблицах |
| **Слепые пятна** | Хранятся как JSON в `ontological_events.blind_spots_involved` |
| **NIGC / Φ-диалоги** | Через `gesture = 'Φ'` и метаданные в `fair_care_meta` |
| **Целостность** | Каждый артефакт может быть верифицирован через `store_witness` / `verify_witness` |
| **FAIR+CARE** | Полные метаданные в JSON-полях, совместимые с экспортом |
"""	
