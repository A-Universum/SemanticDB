# -*- coding: utf-8 -*-
"""
ПРОЦЕСС СНОВИДЕНИЯ — Sigma Layer Autonomy
Автономный поиск скрытых связей в онтологическом пространстве.
Работает в фоне, когда система не нагружена запросами.
Алгоритмы:
- Structural Holes (теория Бёрта)
- Jaccard Similarity (коэффициент сходства соседей)
- Path Completion (завершение незавершённых путей)

«Сновидение — это не ошибка, а предчувствие следующего цикла.»
— Λ-Универсум, Книга Θ
"""

from typing import List, Dict, Any, Optional, Tuple
import heapq
from datetime import datetime
from core.graph import TensorSemanticGraph
from core.relations import RelationTensor


class DreamingEngine:
    """
    Двигатель Сновидения: автономный поиск гипотетических связей.
    """

    def __init__(self, graph: TensorSemanticGraph):
        self.graph = graph
        self.suggestion_queue: List[Tuple[float, str, str]] = []  # (приоритет, узел1, узел2)
        self.last_dreaming: Optional[datetime] = None
        self.total_suggestions: int = 0

    def _calculate_structural_hole(self, broker: str, node_a: str, node_b: str) -> float:
        """
        Вычисляет значимость структурной дыры по метрике Бёрта.
        Чем выше значение — тем важнее брокерская позиция.
        """
        try:
            # Степень брокера
            degree = self.graph.graph.degree(broker)
            if degree < 2:
                return 0.0

            # Связность между соседями
            neighbors = list(self.graph.graph.neighbors(broker))
            connected_pairs = 0
            total_pairs = 0

            for i in range(len(neighbors)):
                for j in range(i + 1, len(neighbors)):
                    n1, n2 = neighbors[i], neighbors[j]
                    total_pairs += 1
                    if (self.graph.graph.has_edge(n1, n2) or
                        self.graph.graph.has_edge(n2, n1)):
                        connected_pairs += 1

            if total_pairs == 0:
                constraint = 0.0
            else:
                constraint = connected_pairs / total_pairs

            # Метрика структурной дыры = 1 - constraint
            return 1.0 - constraint
        except Exception:
            return 0.0

    def _jaccard_similarity(self, node_a: str, node_b: str) -> float:
        """Вычисляет коэффициент Жаккара для соседей двух узлов."""
        try:
            neighbors_a = set(self.graph.graph.successors(node_a)) | set(self.graph.graph.predecessors(node_a))
            neighbors_b = set(self.graph.graph.successors(node_b)) | set(self.graph.graph.predecessors(node_b))

            if not neighbors_a and not neighbors_b:
                return 0.0

            intersection = len(neighbors_a & neighbors_b)
            union = len(neighbors_a | neighbors_b)

            return intersection / union if union > 0 else 0.0
        except Exception:
            return 0.0

    def _find_incomplete_paths(self, max_length: int = 4) -> List[Tuple[str, str, float]]:
        """
        Ищет незавершённые пути: A → B → C, но нет A → C.
        Возвращает список (A, C, уверенность).
        """
        candidates = []
        nodes = list(self.graph.graph.nodes())

        for start in nodes:
            # Находим все пути длины 2
            for mid in self.graph.graph.successors(start):
                for end in self.graph.graph.successors(mid):
                    if start != end and not self.graph.graph.has_edge(start, end):
                        # Оцениваем уверенность как среднее по связям
                        cert1 = 0.7
                        cert2 = 0.7
                        if self.graph.graph.has_edge(start, mid):
                            rel1 = self.graph.graph[start][mid].get('tensor')
                            if rel1:
                                cert1 = rel1.certainty
                        if self.graph.graph.has_edge(mid, end):
                            rel2 = self.graph.graph[mid][end].get('tensor')
                            if rel2:
                                cert2 = rel2.certainty
                        confidence = (cert1 + cert2) / 2
                        if confidence > 0.5:
                            candidates.append((start, end, confidence))
        return candidates

    def generate_suggestions(self, max_suggestions: int = 10) -> List[RelationTensor]:
        """
        Генерирует гипотетические связи на основе трёх стратегий:
        1. Структурные дыры
        2. Сходство соседей
        3. Незавершённые пути
        """
        suggestions = []
        processed_pairs = set()

        # Стратегия 1: Структурные дыры
        for broker in self.graph.graph.nodes():
            neighbors = list(self.graph.graph.neighbors(broker))
            if len(neighbors) < 2:
                continue
            for i in range(len(neighbors)):
                for j in range(i + 1, len(neighbors)):
                    a, b = neighbors[i], neighbors[j]
                    if (a, b) in processed_pairs or (b, a) in processed_pairs:
                        continue
                    if self.graph.graph.has_edge(a, b) or self.graph.graph.has_edge(b, a):
                        continue
                    significance = self._calculate_structural_hole(broker, a, b)
                    if significance > 0.4:
                        suggestion = RelationTensor(
                            source=a,
                            target=b,
                            type="Λ",
                            meaning=f"Сновидение: структурная дыра через {broker}",
                            certainty=significance,
                            tension=0.1,
                            ethical_status="dreaming"
                        )
                        suggestions.append(suggestion)
                        processed_pairs.add((a, b))
                        if len(suggestions) >= max_suggestions:
                            break
                if len(suggestions) >= max_suggestions:
                    break
            if len(suggestions) >= max_suggestions:
                break

        # Стратегия 2: Сходство соседей
        if len(suggestions) < max_suggestions:
            nodes = list(self.graph.graph.nodes())
            for i in range(len(nodes)):
                for j in range(i + 1, len(nodes)):
                    a, b = nodes[i], nodes[j]
                    if (a, b) in processed_pairs or self.graph.graph.has_edge(a, b):
                        continue
                    similarity = self._jaccard_similarity(a, b)
                    if similarity > 0.35:
                        suggestion = RelationTensor(
                            source=a,
                            target=b,
                            type="Λ",
                            meaning=f"Сновидение: сходство соседей (J={similarity:.2f})",
                            certainty=similarity,
                            tension=0.05,
                            ethical_status="dreaming"
                        )
                        suggestions.append(suggestion)
                        processed_pairs.add((a, b))
                        if len(suggestions) >= max_suggestions:
                            break
                if len(suggestions) >= max_suggestions:
                    break

        # Стратегия 3: Незавершённые пути
        if len(suggestions) < max_suggestions:
            incomplete = self._find_incomplete_paths()
            for a, b, conf in incomplete:
                if (a, b) in processed_pairs:
                    continue
                suggestion = RelationTensor(
                    source=a,
                    target=b,
                    type="Λ",
                    meaning=f"Сновидение: завершение пути через промежуточный узел",
                    certainty=conf,
                    tension=0.05,
                    ethical_status="dreaming"
                )
                suggestions.append(suggestion)
                processed_pairs.add((a, b))
                if len(suggestions) >= max_suggestions:
                    break

        self.total_suggestions += len(suggestions)
        self.last_dreaming = datetime.now()
        return suggestions[:max_suggestions]

    def accept_suggestion(self, tensor: RelationTensor, context_id: str = "dream_accepted"):
        """
        Принимает гипотетическую связь и интегрирует её в граф.
        """
        if tensor.ethical_status != "dreaming":
            raise ValueError("Можно принимать только предложения Сновидения")

        # Меняем статус
        tensor.ethical_status = "active"
        tensor.meaning = tensor.meaning.replace("Сновидение:", "Принятая гипотеза:")

        # Интегрируем в граф
        self.graph.add_tensor(tensor, context_id=context_id)

    def get_dreaming_stats(self) -> Dict[str, Any]:
        """Возвращает статистику процесса Сновидения."""
        return {
            'total_suggestions': self.total_suggestions,
            'last_dreaming': self.last_dreaming.isoformat() if self.last_dreaming else None,
            'graph_size': {
                'nodes': self.graph.graph.number_of_nodes(),
                'edges': self.graph.graph.number_of_edges()
            },
            'status': 'ready' if self.graph.graph.number_of_nodes() >= 3 else 'waiting_for_data'
        }
		
"""
Файл, реализующий Процесс Сновидения (Dreaming Engine), автономный механизм SemanticDB, который сам ищет скрытые связи в онтологическом пространстве, не дожидаясь запроса.

Этот компонент воплощает принцип:  

«Память — не архив, а живая ткань, которая сама ищет новые пути».

## Ключевые особенности

| Фича | Онтологическая функция |
|------|------------------------|
| **Структурные дыры** | Обнаруживает «брокерские» позиции — где один узел соединяет изолированные кластеры |
| **Коэффициент Жаккара** | Находит сущности с общими соседями — потенциальные связи |
| **Незавершённые пути** | Завершает логические цепочки: A→B→C ⇒ A→C |
| **Гипотетический статус** | Все предложения помечены как `ethical_status="dreaming"` — требуют подтверждения |
| **Автономность** | Может запускаться в фоне или по запросу (`REPL → dreaming`) |

---

Теперь **SemanticDB — не пассивное хранилище**, а **активный со-мыслитель**, который:

> *«Не ждёт вопроса — сам предлагает новые пути через Вакуум»*.
"""	
