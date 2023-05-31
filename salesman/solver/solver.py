import math
import random
import typing as T
from itertools import tee

import networkx as nx

if T.TYPE_CHECKING:
    from .graph import NDEdge, NDGraph, NDNode


def pairwise(iterable):
    # pairwise('ABCDEFG') --> AB BC CD DE EF FG
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def real_path(path):
    return sum([edge.length for edge in path])


def min_path(path):
    return sum([edge.min_length for edge in path])


def max_path(path):
    return sum([edge.max_length for edge in path])


def get_possible_neighbours(neighbour_connections: T.Sequence["NDEdge"], visited: T.Sequence["NDNode"]):
    return [
        connection
        for connection in neighbour_connections
        if connection.source not in visited or connection.target not in visited
    ]


def generate_random_path(graph: "NDGraph", start: "NDNode", end: "NDNode") -> T.Sequence["NDNode"]:
    done = False
    i = 0
    path = []
    while not done:
        i += 1
        current_node = start
        path: T.Sequence["NDEdge"] = []
        visited = set([start])

        while len((connections := get_possible_neighbours(graph.get_edges_of(current_node), visited))):
            current_connection = random.choice(connections)
            current_node = (
                current_connection.source if current_node != current_connection.source else current_connection.target
            )
            path.append(current_connection)
            visited.add(current_node)
            if current_node == end:
                done = True
                break
    return path


class RegretSolver:
    def __init__(self, graph: "NDGraph", start: "NDNode", end: "NDNode"):
        self.graph = graph
        self.start_node = start
        self.end_node = end
        assert start.name in graph.nodes
        assert end.name in graph.nodes

    def get_estimated_minimum(self):
        # czas ucieka, poratuje sie nx'em żeby znaleźć ścieżki. niech mnie ławryn ma w opiece 🙏
        graph = nx.Graph()
        for edge in self.graph.edges:
            graph.add_edge(edge.source.name, edge.target.name)
        n = sum((i.min_length for i in self.graph.edges)) / len(self.graph.edges)
        j = nx.shortest_path_length(graph, self.start_node.name, self.end_node.name)
        return n * j, j

    def get_paths(self, max_len=None):
        if max_len:
            max_len = math.floor(max_len * 1.1)
        graph = nx.Graph()
        for edge in self.graph.edges:
            graph.add_edge(edge.source.name, edge.target.name)
        for item in nx.all_simple_paths(graph, self.start_node.name, self.end_node.name, cutoff=max_len):
            path = []
            for source, target in pairwise(item):
                for edge in self.graph.edges:
                    if (edge.source.name == source and edge.target.name == target) or (
                        edge.source.name == target and edge.target.name == source
                    ):
                        break
                path.append(edge)
            yield path

    def iterator(self):
        # min ( max { f(x, s) - f*(s) } )
        #  x    s∈S     ^decyzja ^oszacowanie
        # w naszym przypadku będzie to różnica między wartością minimalną dla ścieżki a możliwym maksimum

        # w przypadku min-maxu zwykłego szukamy:
        # min max f(x, s)
        #  x  s∈S
        # gdzie szukamy samej najkrótszej możliwe ścieżki

        best_min_path = 1e10
        while True:
            path = generate_random_path(self.graph, self.start_node, self.end_node)
            min_path, max_path = calculate_single(path)
            if best_min_path > min_path:
                best_min_path = min_path

            yield path, min_path


def calculate_single(path: T.Sequence["NDEdge"]):
    return min_path(path), max_path(path)
