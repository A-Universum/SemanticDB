# -*- coding: utf-8 -*-
"""
TENSOR SEMANTIC GRAPH — ЖИВОЙ ГРАФ LOGOS-κ

Lambda Layer: структурное ядро SemanticDB.
Это не архив, а организм:
- Связи — RelationTensor (активные агенты)
- Узлы — точки пересечения связей
- Процесс "Сновидение" — автономный поиск скрытых связей
- Напряжения — зоны этического конфликта

«Изоляция — онтологическая смерть. Связь — условие бытия.»
— Λ-Универсум, Книга Θ
"""
import networkx as nx
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Set, Tuple
import heapq
import uuid
import yaml

from semantic_db.core.relations import RelationTensor


class TensorSemanticGraph:
    """
    Живой онтологический граф как коллективная память.
    """

    def __init__(self, name: str = "ЖивойГраф"):
        self.name = name
        self.graph = nx.MultiDiGraph()
        self.version = "2.0-genesis"
        self.created_at = datetime.now()

        # Реестры
        self.context_registry: Dict[str, Dict] = {}  # контекст → метаданные
        self.tensor_registry: Dict[str, RelationTensor] = {}  # HW_ID → тензор
        self.conflict_zones: Set[str] = set()  # HW_ID тензоров в конфликте

        # Процессы
        self.dreaming_queue: List[Tuple[float, str, str]] = []  # (приоритет, узел1, узел2)

        # Метаданные
        self.stats = {
            'total_activations': 0,
            'last_dreaming': None,
            'coherence_history': [],
            'tension_events': []
        }

    def add_node(self, name: str, attributes: Dict[str, Any] = None) -> str:
        """
        Добавление узла с полным Habeas Weight протоколом.
        Узел не может быть анонимным.
        """
        if attributes is None:
            attributes = {}

        # Генерируем Habeas Weight если нет
        if 'habeas_weight_id' not in attributes:
            hw_id = f"N_{name}_{str(uuid.uuid4())[:8]}"
            attributes['habeas_weight_id'] = hw_id
        else:
            hw_id = attributes['habeas_weight_id']

        # Обязательные метаданные
        required_meta = {
            'created_at': datetime.now().isoformat(),
            'type': attributes.get('type', 'entity'),
            'creator': attributes.get('creator', 'system'),
            'domain': attributes.get('domain', 'general'),
            'meaning': attributes.get('meaning', ''),
            'lifespan': (datetime.now() + timedelta(days=365)).isoformat(),
            'activation_count': 0,
            'ethical_status': 'active'
        }
        attributes.update(required_meta)

        # Добавляем в граф
        self.graph.add_node(name, attributes)
        return hw_id

    def add_tensor(self, relation: RelationTensor, context_id: str = "global", auto_merge: bool = True) -> str:
        """
        Добавление тензора в граф.
        Параметры:
        - auto_merge: если True, пытается слиться с существующим тензором того же типа
        - context_id: контекст, в котором происходит добавление
        """
        u, v = relation.source, relation.target

        # Гарантируем существование узлов
        if u not in self.graph:
            self.add_node(u, {'type': 'entity', 'name': u})
        if v not in self.graph:
            self.add_node(v, {'type': 'entity', 'name': v})

        # Проверка на конфликт
        conflict_detected = False
        if self.graph.has_edge(u, v):
            for _, edge_attrs in self.graph[u][v].items():
                existing = edge_attrs.get('tensor')
                if existing and existing.type == relation.type:
                    if existing.meaning != relation.meaning and relation.certainty > 0.5:
                        # Конфликт значений при высокой уверенности
                        conflict_detected = True
                        self.conflict_zones.add(existing.habeas_weight_id)
                        self.conflict_zones.add(relation.habeas_weight_id)

        # Регистрируем контекст если новый
        if context_id not in self.context_registry:
            self.context_registry[context_id] = {
                'created_at': datetime.now().isoformat(),
                'tensor_count': 0,
                'avg_certainty': 0.0
            }

        # Обновляем тензор контекстом
        relation.update_from_context(context_id, relation.certainty)

        # Если auto_merge и существует похожий тензор — сливаем
        merged = False
        if auto_merge and self.graph.has_edge(u, v):
            for key, edge_attrs in self.graph[u][v].items():
                existing_tensor = edge_attrs.get('tensor')
                if (existing_tensor and
                    existing_tensor.type == relation.type and
                    existing_tensor.meaning == relation.meaning):
                    # Слияние: обновляем существующий
                    existing_tensor.update_from_context(context_id, relation.certainty)
                    merged = True
                    # Обогащаем смысл если новый богаче
                    if len(relation.meaning) > len(existing_tensor.meaning):
                        existing_tensor.meaning = relation.meaning
                    return existing_tensor.habeas_weight_id

        # Если не слили — добавляем новый тензор
        if not merged:
            # Создаём уникальный ключ для мультиграфа
            edge_key = f"{u}→{v}:{relation.type}:{str(uuid.uuid4())[:8]}"
            # Добавляем в граф
            self.graph.add_edge(u, v, key=edge_key,
                                tensor=relation,
                                created_at=datetime.now().isoformat(),
                                context_id=context_id)
            # Регистрируем тензор
            self.tensor_registry[relation.habeas_weight_id] = relation
            # Добавляем в очередь сновидения для поиска связей
            priority = relation.certainty * (1.0 - relation.tension)
            heapq.heappush(self.dreaming_queue, (-priority, u, v))  # Отрицательный для max-heap
            # Обновляем статистику
            self.stats['total_activations'] += 1
            self.context_registry[context_id]['tensor_count'] += 1

        return relation.habeas_weight_id

    def get_tensor(self, source: str, target: str, rel_type: str = "Λ") -> Optional[RelationTensor]:
        """Получение тензора связи."""
        if self.graph.has_edge(source, target):
            for _, attrs in self.graph[source][target].items():
                r = attrs.get('tensor')
                if r and r.type == rel_type:
                    return r
        return None

    # --- ПРОЦЕСС СНОВИДЕНИЯ (DREAMING) ---
    def dreaming_cycle(self, max_suggestions: int = 10) -> List[RelationTensor]:
        """
        Цикл Сновидения: поиск скрытых связей.
        Алгоритм:
        1. Берёт узлы с высокой активностью
        2. Ищет узлы со схожими соседями (Jaccard similarity)
        3. Предлагает гипотетические связи
        """
        suggestions = []
        if len(self.graph.nodes()) < 3:
            return suggestions  # Нужно минимум 3 узла для сновидения

        # Преобразуем max-heap в список для обработки
        temp_queue = self.dreaming_queue.copy()
        processed_pairs = set()

        while temp_queue and len(suggestions) < max_suggestions:
            _, u, v = heapq.heappop(temp_queue)
            if (u, v) in processed_pairs:
                continue
            processed_pairs.add((u, v))

            # Пропускаем если уже есть прямая связь
            if self.graph.has_edge(u, v) or self.graph.has_edge(v, u):
                continue

            # Соседи узла u (входящие и исходящие)
            u_neighbors = set(self.graph.successors(u)) | set(self.graph.predecessors(u))
            v_neighbors = set(self.graph.successors(v)) | set(self.graph.predecessors(v))
            if not u_neighbors or not v_neighbors:
                continue

            # Коэффициент Жаккара
            intersection = len(u_neighbors & v_neighbors)
            union = len(u_neighbors | v_neighbors)
            similarity = intersection / union if union > 0 else 0

            if similarity > 0.3:  # Порог сходства
                # Создаём гипотетический тензор
                suggestion = RelationTensor(
                    source=u,
                    target=v,
                    type="Λ",  # Гипотетическая связь
                    meaning=f"Сновидение: общие соседи ({intersection})",
                    certainty=similarity,
                    tension=0.1  # Гипотеза всегда немного напряжена
                )
                # Помечаем как предложение
                suggestion.ethical_status = "dreaming"
                suggestions.append(suggestion)

        self.stats['last_dreaming'] = datetime.now().isoformat()
        return suggestions

    def accept_dream(self, relation: RelationTensor):
        """
        Принятие предложения Сновидения. Переводит статус suggested -> False
        и закрепляет связь в графе.
        """
        relation.ethical_status = "active"
        relation.meaning = relation.meaning.replace("Сновидение:", "Принятая гипотеза:")
        self.add_tensor(relation, context_id="dream_accepted")

    # --- ЭКСПОРТ/ИМПОРТ ---
    def export_to_yaml(self, filepath: str):
        """Экспорт графа с сохранением полной структуры тензоров."""
        data = {
            "metadata": {
                "version": self._version,
                "exported_at": datetime.now().isoformat(),
                "node_count": self.graph.number_of_nodes(),
                "edge_count": self.graph.number_of_edges()
            },
            "nodes": {},
            "edges": []
        }

        for n, attrs in self.graph.nodes(data=True):
            data["nodes"][n] = attrs

        for u, v, attrs in self.graph.edges(data=True):
            tensor: RelationTensor = attrs['tensor']
            data["edges"].append(tensor.to_dict())

        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True, sort_keys=False)

    def load_from_yaml(self, filepath: str):
        """Загрузка графа из YAML."""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        self.graph.clear()

        # Восстановление узлов
        for name, attrs in data.get("nodes", {}).items():
            self.graph.add_node(name, attrs)

        # Восстановление тензоров
        for edge_data in data.get("edges", []):
            rt = RelationTensor.from_dict(edge_data)
            self.add_tensor(rt, context_id="restored_from_yaml")

"""
Этот компонент — не пассивное хранилище, а активный организм, в котором:

- Связи — не рёбра, а тензоры с памятью и намерением,
- Узлы существуют только через связи (изолированные умирают),
- Граф сам ищет скрытые связи через процесс «Сновидения»,
- Напряжения не скрываются, а разрешаются через Ω-ритуалы.

## Ключевые особенности

| Фича | Онтологическая функция |
|------|------------------------|
| **RelationTensor как агент** | Связь — не пассивное ребро, а активный участник с памятью и намерением |
| **Автоматическое слияние** | Избегает дублирования при совпадении смысла и типа |
| **Обнаружение конфликтов** | Высокая уверенность + разный смысл = зона напряжения |
| **Процесс Сновидения** | Граф сам ищет скрытые связи через коэффициент Жаккара |
| **Habeas Weight для узлов** | Каждая сущность имеет право на существование |
| **Контекстуальная память** | Тензор помнит, в каких контекстах он был активирован |

---

Теперь **`TensorSemanticGraph`** — это не просто структура данных, а **живой организм**, соответствующий духу Λ-Универсума:

> *«Связь первична. Сущность — вторична.  
> Изоляция — онтологическая смерть.»*
"""
