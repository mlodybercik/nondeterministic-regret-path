from sys import maxsize as max_hash_size
from typing import Any, Dict, List, Optional, Set, Tuple, Union

import numpy as np


def hash_nodes(source: "NDNode", target: "NDNode"):
    return (hash(source) * hash(target)) % max_hash_size


class NDNode:
    params: Dict[str, Any]
    name: str
    __slots__ = ["params", "name"]

    def __init__(self, name: str, **params: Dict[str, Any]) -> None:
        self.name = name
        self.params = params

    def __getitem__(self, *a):
        return self.params.__getitem__(*a)

    def __setitem__(self, *a):
        return self.params.__setitem__(*a)

    def __delitem__(self, *a):
        return self.params.__delitem__(*a)

    def __repr__(self) -> str:
        return f"<{__class__.__name__} name={self.name}>"

    def __hash__(self):
        return hash(self.name)


class NDEdge:
    possible_length: Tuple[float, float]
    length: float

    @property
    def min_length(self):
        return self.possible_length[0]

    @property
    def max_length(self):
        return self.possible_length[1]

    def __init__(self, source: "NDNode", target: "NDNode", min_length: float, max_length: float, length: float):
        self.source = source
        self.target = target
        if not (max_length > min_length):
            raise ValueError(f"max < min, {max_length} < {min_length}")
        if not (length >= min_length and length <= max_length):
            raise ValueError(f"length not between min and max, {min_length} >= {length} >= {max_length}")

        self.possible_length = (min_length, max_length)
        self.length = length

    @classmethod
    def from_min_max(cls, source: "NDNode", target: "NDNode", min_length: float, max_length: float):
        return cls(source, target, min_length, max_length, np.random.uniform(min_length, max_length))

    @classmethod
    def from_random(cls, source: "NDNode", target: "NDNode", scale: float):
        min_value, max_value = sorted([scale * np.random.uniform(0, 1), scale * np.random.uniform(0, 1)])
        return cls.from_min_max(source, target, min_value, max_value)
        # return cls.from_min_max(source, target, 0.95, 1.05)

    def __hash__(self):
        # nie wiem czy nie lepiej zostawić tu samo dodawanie
        return hash_nodes(self.source, self.target)

    def __repr__(self):
        return f"<{__class__.__name__} source={self.source.name} target={self.target.name}>"


class NDGraph:
    nodes: Dict[str, NDNode]
    edges: Set[NDEdge]

    def __init__(self):
        self.nodes = dict()
        self.edges = set()

    def add_from_edge(self, edge: "NDEdge"):
        # dodajemy do naszej bazy wierzchołki, jeśli one już istnieją to to nic nie zmieni
        # jeśli nie istnieją to tutaj zostaną dodane do naszego grafu
        self.nodes[edge.source.name] = edge.source
        self.nodes[edge.target.name] = edge.target
        # korzystanie ze zbioru sprawi że nie bedziemy mieli powtórzeń w krawędziach
        # hashujemy [dodając|mnożąc przez siebie] hashe wierzchołków więc jesteśmy
        # w stanie sprawdzić czy dane połączenie już istnieje, jeśli to istnieje
        # to set.add nic nie zmieni
        self.edges.add(edge)

    def add_edge(
        self,
        source: Union["NDNode", str],
        target: Union["NDNode", str],
        lengths: Optional[Tuple[float, float]] = None,
        scale: Optional[float] = None,
    ):
        # sprawdz czy dane wierzcholki istnieja jak tak to wybierz ze znanych
        # wpw stwórz nowe
        if isinstance(source, str):
            source = self.nodes.get(source, NDNode(source))
        if isinstance(target, str):
            target = self.nodes.get(target, NDNode(target))
        # stwórz wierzchołki wg zadanych parametrów
        # jeśli podane jest min/max to zrób według tego
        # wpw samemu stwórz skalę
        if lengths:
            return self.add_from_edge(NDEdge.from_min_max(source, target, lengths[0], lengths[1]))
        elif scale:
            return self.add_from_edge(NDEdge.from_random(source, target, scale))
        raise ValueError("none of the required params passed")

    def get_edges_of(self, node: Union[str, NDNode]):
        if isinstance(node, str):
            node = self.nodes[node]
        return {edge for edge in self.edges if edge.source == node or edge.target == node}

    def get_neighbors(self, node: Union[str, NDNode]):
        if isinstance(node, str):
            node = self.nodes[node]
        return {(i.source if i.source != node else i.target) for i in self.get_edges_of(node)}

    def get_nodes(self):
        return set(self.nodes.keys())

    def get_spring_layout(self, k=1e-3, max_iterations=1000):
        positions = {}
        length = len(self.nodes)
        for i, node in enumerate(self.nodes.values()):
            positions[node] = np.array([np.sin(2 * np.pi * i / length), np.cos(2 * np.pi * i / length)])

        # pętla główna algorytmu
        for _ in range(max_iterations):
            # obliczanie sił między wierzchołkami połączonymi krawędzią
            forces = {j: [0, 0] for j in self.nodes.values()}
            for connection in self.edges:
                node_a = connection.source
                node_b = connection.target

                d = positions[node_b] - positions[node_a]
                distance = np.sqrt(np.sum(d * d))
                desired = connection.length

                f = -k * (distance - desired) / np.sqrt(distance + 1e-9)

                forces[node_a] -= f * d / 2
                forces[node_b] += f * d / 2

            # aktualizacja położeń wierzchołków
            for node in self.nodes.values():
                positions[node] += forces[node]

        min_pos = np.array([np.inf, np.inf])
        max_pos = np.array([-np.inf, -np.inf])
        for node in positions:
            if min_pos[0] > positions[node][0]:
                min_pos[0] = positions[node][0]
            elif max_pos[0] < positions[node][0]:
                max_pos[0] = positions[node][0]

            if min_pos[1] > positions[node][1]:
                min_pos[1] = positions[node][1]
            elif max_pos[1] < positions[node][1]:
                max_pos[1] = positions[node][1]

        for node in positions:
            positions[node] = (positions[node] - min_pos) / (max_pos - min_pos)

        return positions

    @classmethod
    def barabasi_albert(cls, n: int, m: int):
        raise NotImplementedError()

    @classmethod
    def watts_strogatz(cls, n: int, p: float, lengths_scale: int, k=2):
        assert n > 5
        nodes = [NDNode(str(i)) for i in range(n)]
        edges: List[NDEdge] = []
        for i, node in enumerate(nodes):
            for j in range(1, k + 1):
                edges.append(NDEdge.from_random(node, nodes[i - j], lengths_scale))
                edges.append(NDEdge.from_random(node, nodes[(i + j) % n], lengths_scale))

        for i in range(n):
            if np.random.random() > p:
                while (new_edge := np.random.choice(nodes)) == edges[i].source:
                    continue
                edges[i].target = new_edge

        graph = cls()
        [graph.add_from_edge(i) for i in edges]
        return graph
