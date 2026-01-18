# -*- coding: utf-8 -*-
"""
ДВИГАТЕЛЬ КОГЕРЕНТНОСТИ — Sigma Layer
Онтологический иммунитет SemanticDB.
Вычисляет, диагностирует, предлагает действия.
«Когерентность — не истина, а условие состоятельности.»
— Λ-Универсум, Книга Θ
"""
from typing import Dict, List, Any, Tuple, Optional
from datetime import datetime, timedelta
import math
import networkx as nx


class CoherenceEngine:
    """
    Двигатель когерентности: мозг живого графа.
    """

    def __init__(self, graph):
        self.graph = graph  # TensorSemanticGraph
        self.history: List[Tuple[datetime, float]] = []
        self.tension_log: List[Dict] = []
        self.coherence_thresholds = {
            'healthy': 0.7,
            'warning': 0.4,
            'crisis': 0.2
        }

    def calculate_global_coherence(self) -> Dict[str, Any]:
        """
        Вычисляет многомерную когерентность графа.
        Возвращает:
        - global: взвешенная метрика
        - structural: связность графа
        - semantic: средняя уверенность связей
        - tension_penalty: штраф за напряжения
        """
        if self.graph.graph.number_of_nodes() == 0:
            return self._empty_graph_result()

        # 1. Структурная когерентность (связность)
        structural = self._calculate_structural_coherence()

        # 2. Семантическая когерентность (уверенность связей)
        semantic, total_certainty, total_tension = self._calculate_semantic_coherence()

        # 3. Штраф за напряжения
        tension_penalty = self._calculate_tension_penalty(total_tension)

        # 4. Глобальная когерентность (взвешенная)
        global_coherence = (
            structural * 0.3 +
            semantic * 0.5 +
            (1.0 - tension_penalty) * 0.2
        )

        # Ограничиваем диапазон
        global_coherence = max(0.0, min(1.0, global_coherence))

        # Сохраняем в историю
        now = datetime.now()
        self.history.append((now, global_coherence))
        # Ограничиваем историю
        if len(self.history) > 1000:
            self.history = self.history[-500:]

        result = {
            'global': global_coherence,
            'structural': structural,
            'semantic': semantic,
            'tension_penalty': tension_penalty,
            'metrics': {
                'nodes': self.graph.graph.number_of_nodes(),
                'edges': self.graph.graph.number_of_edges(),
                'isolated_nodes': self._count_isolated_nodes(),
                'high_tension_relations': total_tension,
                'avg_certainty': total_certainty
            },
            'status': self._get_status(global_coherence),
            'timestamp': now.isoformat()
        }

        return result

    def _empty_graph_result(self) -> Dict[str, Any]:
        """Результат для пустого графа."""
        return {
            'global': 1.0,  # Пустота — идеально когерентна
            'structural': 1.0,
            'semantic': 1.0,
            'tension_penalty': 0.0,
            'metrics': {'nodes': 0, 'edges': 0, 'isolated_nodes': 0, 'high_tension_relations': 0, 'avg_certainty': 1.0},
            'status': 'empty',
            'timestamp': datetime.now().isoformat()
        }

    def _calculate_structural_coherence(self) -> float:
        """Вычисляет структурную когерентность (связность)."""
        try:
            # Плотность графа
            density = nx.density(self.graph.graph)
            # Число компонент связности
            components = nx.number_weakly_connected_components(self.graph.graph)
            # Нормализуем компоненты
            if self.graph.graph.number_of_nodes() == 0:
                component_score = 1.0
            else:
                component_score = 1.0 / max(1, components)
            # Взвешиваем
            structural = density * 0.4 + component_score * 0.6
            return max(0.0, min(1.0, structural))
        except Exception:
            return 0.0

    def _calculate_semantic_coherence(self) -> Tuple[float, float, int]:
        """Вычисляет семантическую когерентность и статистику напряжений."""
        total_certainty = 0.0
        total_tension = 0
        edge_count = 0

        for _, _, attrs in self.graph.graph.edges(data=True):
            tensor = attrs.get('tensor')
            if tensor:
                total_certainty += tensor.certainty
                if tensor.tension > 0.7:
                    total_tension += 1
                edge_count += 1

        avg_certainty = total_certainty / edge_count if edge_count > 0 else 1.0
        semantic = avg_certainty
        return semantic, avg_certainty, total_tension

    def _calculate_tension_penalty(self, high_tension_count: int) -> float:
        """Вычисляет штраф за напряжения."""
        if high_tension_count == 0:
            return 0.0
        # Логарифмический штраф
        penalty = min(1.0, math.log1p(high_tension_count) / 10.0)
        return penalty

    def _count_isolated_nodes(self) -> int:
        """Считает изолированные узлы (онтологическая смерть)."""
        return sum(
            1 for node in self.graph.graph.nodes()
            if self.graph.graph.degree(node) == 0
        )

    def _get_status(self, coherence: float) -> str:
        """Определяет статус по уровню когерентности."""
        if coherence >= self.coherence_thresholds['healthy']:
            return 'healthy'
        elif coherence >= self.coherence_thresholds['warning']:
            return 'warning'
        elif coherence >= self.coherence_thresholds['crisis']:
            return 'crisis'
        else:
            return 'collapse'

    def detect_tensions(self) -> List[Dict[str, Any]]:
        """
        Обнаруживает зоны напряжения:
        - Конфликтующие связи (одинаковый тип, разный смысл)
        - Циклы с высоким напряжением
        - Изолированные узлы с высокой активностью
        """
        tensions = []

        # 1. Конфликтующие связи
        for u in self.graph.graph.nodes():
            for v in self.graph.graph.nodes():
                if u == v:
                    continue
                if self.graph.graph.has_edge(u, v):
                    tensors = []
                    for _, attrs in self.graph.graph[u][v].items():
                        t = attrs.get('tensor')
                        if t:
                            tensors.append(t)
                    # Ищем конфликты
                    for i in range(len(tensors)):
                        for j in range(i + 1, len(tensors)):
                            t1, t2 = tensors[i], tensors[j]
                            if (t1.type == t2.type and
                                t1.meaning != t2.meaning and
                                t1.certainty > 0.6 and t2.certainty > 0.6):
                                tensions.append({
                                    'type': 'meaning_conflict',
                                    'source': u,
                                    'target': v,
                                    'tensor_ids': [t1.habeas_weight_id, t2.habeas_weight_id],
                                    'severity': 'high'
                                })

        # 2. Циклы с напряжением
        try:
            cycles = list(nx.simple_cycles(nx.DiGraph(self.graph.graph)))
            for cycle in cycles:
                if len(cycle) > 2:  # Игнорируем двойные циклы
                    # Проверяем напряжение в цикле
                    avg_tension = 0.0
                    count = 0
                    for i in range(len(cycle)):
                        u, v = cycle[i], cycle[(i + 1) % len(cycle)]
                        if self.graph.graph.has_edge(u, v):
                            for _, attrs in self.graph.graph[u][v].items():
                                t = attrs.get('tensor')
                                if t:
                                    avg_tension += t.tension
                                    count += 1
                    if count > 0:
                        avg_tension /= count
                        if avg_tension > 0.6:
                            tensions.append({
                                'type': 'tense_cycle',
                                'cycle': cycle,
                                'avg_tension': avg_tension,
                                'severity': 'medium'
                            })
        except Exception:
            pass  # Игнорируем ошибки в больших графах

        # 3. Изолированные узлы
        isolated = self._count_isolated_nodes()
        if isolated > 0:
            tensions.append({
                'type': 'isolation',
                'count': isolated,
                'severity': 'low'
            })

        # Сохраняем в лог
        self.tension_log.extend(tensions)
        # Ограничиваем лог
        if len(self.tension_log) > 1000:
            self.tension_log = self.tension_log[-500:]

        return tensions

    def get_coherence_trend(self, window_hours: int = 24) -> Dict[str, Any]:
        """
        Анализирует тренд когерентности за последние N часов.
        """
        if not self.history:
            return {'trend': 'stable', 'change': 0.0, 'data_points': 0}

        cutoff = datetime.now() - timedelta(hours=window_hours)
        recent = [(t, c) for t, c in self.history if t >= cutoff]

        if len(recent) < 2:
            return {'trend': 'insufficient_data', 'change': 0.0, 'data_points': len(recent)}

        first = recent[0][1]
        last = recent[-1][1]
        change = last - first

        if change > 0.05:
            trend = 'improving'
        elif change < -0.05:
            trend = 'degrading'
        else:
            trend = 'stable'

        return {
            'trend': trend,
            'change': change,
            'data_points': len(recent),
            'first': first,
            'last': last,
            'window_hours': window_hours
        }

    def diagnose(self) -> Dict[str, Any]:
        """
        Полная диагностика состояния онтологического пространства.
        """
        coherence = self.calculate_global_coherence()
        tensions = self.detect_tensions()
        trend = self.get_coherence_trend()

        # Генерация рекомендаций
        recommendations = []
        status = coherence['status']

        if status == 'crisis' or status == 'collapse':
            recommendations.append("Активировать Ω-автомат: признать предел")
        if coherence['metrics']['isolated_nodes'] > 5:
            recommendations.append("Создать связи (Λ) для изолированных сущностей")
        if len([t for t in tensions if t['severity'] == 'high']) > 0:
            recommendations.append("Инициировать Φ-диалог для разрешения конфликтов")
        if trend['trend'] == 'degrading':
            recommendations.append("Провести ∇-обогащение инвариантами")

        return {
            'coherence': coherence,
            'tensions': tensions,
            'trend': trend,
            'recommendations': recommendations,
            'diagnosis_timestamp': datetime.now().isoformat()
        }
		
"""
Этот компонент — не просто «метрика», а онтологический иммунитет, который:

- Непрерывно вычисляет глобальную когерентность графа,
- Обнаруживает зоны напряжения (конфликты, противоречия),
- Предлагает Ω-ритуалы для разрешения конфликтов,
- Отслеживает динамику во времени (тренды, кризисы, рост).

## Ключевые особенности

| Фича | Онтологическая функция |
|------|------------------------|
| **Многомерная когерентность** | Учитывает структуру, семантику и напряжения |
| **Обнаружение конфликтов** | Находит противоречащие связи с высокой уверенностью |
| **Анализ циклов** | Выявляет напряжённые петли в графе |
| **Тренды во времени** | Отслеживает деградацию или улучшение |
| **Рекомендации** | Не просто диагноз, а призыв к действию (Ω, Φ, ∇) |
| **История** | Сохраняет динамику для анализа |

---

Теперь **`CoherenceEngine`** — это не «аналитика», а **онтологический иммунитет**, который:

> *«Не скрывает болезнь, а превращает её в условие трансформации»*.
"""		
