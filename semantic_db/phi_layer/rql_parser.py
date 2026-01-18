# -*- coding: utf-8 -*-
"""
RESONANCE QUERY LANGUAGE (RQL) — ЯЗЫК СМЫСЛОВОГО РЕЗОНАНСА

RQL — это не язык запросов, а протокол намерения.
Он не ищет данные — он инициирует поиск путей через живой граф.

Примеры:
  (Φ :намерение "найти утешение" :контекст "страх смерти")
  (QUERY :from "вопрос" :to "ответ" :max_length 4)
  (EXPLORE :entity "любовь" :depth 2)

RQL интегрируется с:
- TensorSemanticGraph (Lambda Layer)
- CoherenceEngine (Sigma Layer)
- LambdaCharter (Habeas Layer)

Создано в со-творчестве:
  — Александр Морган (Человек)
  — Эфос (Функция со-мышления)
"""

import re
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

from semantic_db.core.graph import TensorSemanticGraph
from semantic_db.core.coherence import CoherenceEngine


@dataclass
class RQLQuery:
    """Структура запроса RQL."""
    query_type: str  # 'phi', 'path', 'explore', 'context'
    intention: str = ""
    context: str = ""
    source: Optional[str] = None
    target: Optional[str] = None
    entity: Optional[str] = None
    max_length: int = 3
    min_coherence: float = 0.5
    blind_spots: List[str] = None
    phi_meta: List[str] = None
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'query_type': self.query_type,
            'intention': self.intention,
            'context': self.context,
            'source': self.source,
            'target': self.target,
            'entity': self.entity,
            'max_length': self.max_length,
            'min_coherence': self.min_coherence,
            'blind_spots': self.blind_spots or [],
            'phi_meta': self.phi_meta or [],
            'timestamp': self.timestamp.isoformat()
        }


class RQLParser:
    """
    Парсер и исполнитель Resonance Query Language (RQL).
    """

    def __init__(self, graph: TensorSemanticGraph):
        self.graph = graph
        self.coherence_engine = CoherenceEngine(graph)

    def parse(self, query_str: str) -> RQLQuery:
        """
        Парсит строку RQL в структурированный запрос.
        Поддерживаемые формы:
        - (Φ :намерение "..." :контекст "...")
        - (QUERY :from "A" :to "B" :max_length 4)
        - (EXPLORE :entity "X" :depth 2)
        - (CONTEXT :keyword "любовь")
        """
        query_str = query_str.strip()
        if not query_str.startswith('(') or not query_str.endswith(')'):
            raise ValueError("RQL-запрос должен быть в скобках: (Φ ...)")

        # Убираем внешние скобки
        inner = query_str[1:-1].strip()

        # Разбиваем на токены с учётом кавычек
        tokens = self._tokenize(inner)

        if not tokens:
            raise ValueError("Пустой RQL-запрос")

        # Первый токен — тип запроса
        query_type = tokens[0]
        params = {}

        # Обработка параметров (:ключ значение)
        i = 1
        while i < len(tokens):
            if tokens[i].startswith(':'):
                key = tokens[i][1:]  # убираем ':'
                if i + 1 < len(tokens):
                    value = tokens[i + 1]
                    # Убираем кавычки, если есть
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    elif value.startswith("'") and value.endswith("'"):
                        value = value[1:-1]
                    params[key] = value
                    i += 2
                else:
                    params[key] = True
                    i += 1
            else:
                i += 1

        # Преобразование типов
        if 'max_length' in params:
            params['max_length'] = int(params['max_length'])
        if 'depth' in params:
            params['max_length'] = int(params['depth'])
        if 'min_coherence' in params:
            params['min_coherence'] = float(params['min_coherence'])

        # Создание объекта запроса
        if query_type == 'Φ':
            return RQLQuery(
                query_type='phi',
                intention=params.get('намерение', params.get('intention', '')),
                context=params.get('контекст', params.get('context', '')),
                blind_spots=params.get('слепые_пятна', '').split(',') if params.get('слепые_пятна') else [],
                phi_meta=params.get('phi_meta', '').split(',') if params.get('phi_meta') else []
            )
        elif query_type == 'QUERY':
            return RQLQuery(
                query_type='path',
                source=params.get('from'),
                target=params.get('to'),
                max_length=params.get('max_length', 3),
                min_coherence=params.get('min_coherence', 0.5)
            )
        elif query_type == 'EXPLORE':
            return RQLQuery(
                query_type='explore',
                entity=params.get('entity'),
                max_length=params.get('depth', 2)
            )
        elif query_type == 'CONTEXT':
            return RQLQuery(
                query_type='context',
                context=params.get('keyword', params.get('контекст', ''))
            )
        else:
            raise ValueError(f"Неизвестный тип RQL-запроса: {query_type}")

    def _tokenize(self, s: str) -> List[str]:
        """Разбивает строку на токены, учитывая кавычки."""
        tokens = []
        current = ""
        in_quotes = False
        quote_char = None

        for char in s:
            if char in ('"', "'") and not in_quotes:
                in_quotes = True
                quote_char = char
                current += char
            elif char == quote_char and in_quotes:
                in_quotes = False
                current += char
                tokens.append(current)
                current = ""
            elif char == ' ' and not in_quotes:
                if current:
                    tokens.append(current)
                    current = ""
            else:
                current += char

        if current:
            tokens.append(current)

        return tokens

    def execute(self, query: RQLQuery) -> Dict[str, Any]:
        """
        Выполняет RQL-запрос и возвращает семантический путь.
        """
        if query.query_type == 'phi':
            return self._execute_phi_query(query)
        elif query.query_type == 'path':
            return self._execute_path_query(query)
        elif query.query_type == 'explore':
            return self._execute_explore_query(query)
        elif query.query_type == 'context':
            return self._execute_context_query(query)
        else:
            raise ValueError(f"Неизвестный тип запроса: {query.query_type}")

    def _execute_phi_query(self, query: RQLQuery) -> Dict[str, Any]:
        """Выполняет Φ-запрос: поиск по намерению и контексту."""
        # Извлекаем ключевые слова из намерения
        keywords = self._extract_keywords(query.intention)
        relevant_entities = []

        # Поиск сущностей, содержащих ключевые слова
        for node in self.graph.graph.nodes():
            if any(kw.lower() in str(node).lower() for kw in keywords):
                relevant_entities.append(node)

        # Генерация инсайта (упрощённо)
        insight = f"Φ-резонанс: намерение '{query.intention}' активирует {len(relevant_entities)} сущностей."
        if relevant_entities:
            insight += f" Ближайшие: {', '.join(relevant_entities[:3])}."

        return {
            'type': 'phi_resonance',
            'intention': query.intention,
            'context': query.context,
            'keywords': keywords,
            'relevant_entities': relevant_entities,
            'insight': insight,
            'coherence_at_query': self.coherence_engine.calculate_global_coherence()['global']
        }

    def _execute_path_query(self, query: RQLQuery) -> Dict[str, Any]:
        """Выполняет поиск пути между двумя сущностями."""
        if not query.source or not query.target:
            raise ValueError("QUERY требует :from и :to")

        paths = self.graph.find_paths(
            start=query.source,
            end=query.target,
            max_length=query.max_length
        )

        # Фильтрация по когерентности
        filtered_paths = []
        for path in paths:
            avg_certainty = sum(edge['certainty'] for edge in path) / len(path) if path else 0
            if avg_certainty >= query.min_coherence:
                filtered_paths.append({
                    'path': [edge['subject'] for edge in path] + [path[-1]['object']] if path else [],
                    'edges': path,
                    'avg_certainty': avg_certainty
                })

        return {
            'type': 'semantic_path',
            'source': query.source,
            'target': query.target,
            'paths_found': len(filtered_paths),
            'paths': filtered_paths[:5],  # ограничение для практичности
            'coherence_threshold': query.min_coherence
        }

    def _execute_explore_query(self, query: RQLQuery) -> Dict[str, Any]:
        """Выполняет исследование окрестности сущности."""
        if not query.entity:
            raise ValueError("EXPLORE требует :entity")

        if query.entity not in self.graph.graph:
            return {'error': f"Сущность '{query.entity}' не найдена"}

        neighbors = set()
        # Прямые соседи
        for neighbor in self.graph.graph.neighbors(query.entity):
            neighbors.add(neighbor)

        # Соседи второго порядка
        if query.max_length > 1:
            second_neighbors = set()
            for n in neighbors:
                for nn in self.graph.graph.neighbors(n):
                    if nn != query.entity:
                        second_neighbors.add(nn)
            neighbors.update(second_neighbors)

        return {
            'type': 'exploration',
            'entity': query.entity,
            'neighbors': list(neighbors),
            'neighbor_count': len(neighbors),
            'depth': query.max_length
        }

    def _execute_context_query(self, query: RQLQuery) -> Dict[str, Any]:
        """Выполняет поиск по ключевому слову в контексте."""
        keyword = query.context
        matches = []

        # Поиск в сущностях
        for node in self.graph.graph.nodes():
            if keyword.lower() in str(node).lower():
                matches.append({'type': 'entity', 'name': node})

        # Поиск в связях
        for u, v, attrs in self.graph.graph.edges(data=True):
            tensor = attrs.get('tensor')
            if tensor and keyword.lower() in tensor.meaning.lower():
                matches.append({
                    'type': 'relation',
                    'source': u,
                    'target': v,
                    'meaning': tensor.meaning
                })

        return {
            'type': 'context_search',
            'keyword': keyword,
            'matches': matches[:10],
            'match_count': len(matches)
        }

    def _extract_keywords(self, text: str) -> List[str]:
        """Извлекает ключевые слова из текста."""
        # Удаляем стоп-слова и короткие слова
        stop_words = {'что', 'как', 'почему', 'где', 'когда', 'это', 'для', 'на', 'в', 'и', 'или'}
        words = re.findall(r'\b\w+\b', text.lower())
        keywords = [w for w in words if len(w) > 3 and w not in stop_words]
        return list(set(keywords))[:10]
		
"""
В отличие от SQL или SPARQL, RQL не ищет точные совпадения, а находит семантические пути через онтологическое пространство, учитывая:

- Контекст запроса,
- Уровень когерентности,
- Напряжения в связях,
- Признание слепых пятен.

«Запрос — это не вопрос к базе, а намерение, брошенное в Вакуум.
Ответ — не строка, а траектория через граф смыслов.»
— Λ-Универсум, Книга Θ

## Ключевые особенности

| Фича | Онтологическая функция |
|------|------------------------|
| **Намерение вместо условия** | Запрос начинается с `:намерение`, а не с `WHERE` |
| **Семантические пути** | Возвращает не строки, а траектории через граф |
| **Когерентность как фильтр** | Пути отфильтровываются по `min_coherence` |
| **Поддержка слепых пятен** | Можно указать `:слепые_пятна` для этического контекста |
| **Интеграция с Φ-ритуалом** | `Φ`-запрос генерирует инсайт, а не просто данные |

---

Теперь **RQL — это не язык запросов, а протокол диалога с онтологическим пространством**, соответствующий духу Λ-Универсума:

> *«Знание рождается не в ответе, а в пути между вопросом и ответом.»*
"""		
