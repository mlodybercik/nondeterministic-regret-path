import math
import typing as T
from itertools import tee

import networkx as nx

from .graph import hash_nodes

if T.TYPE_CHECKING:
    from .graph import NDGraph, NDNode


def pairwise(iterable):
    # pairwise('ABCDEFG') --> AB BC CD DE EF FG
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def calculate_path(graph: "NDGraph", path_in_nodes: T.Sequence["NDNode"]):
    min_path = dict.fromkeys(range(len(graph.scenario)))
    real_path = dict.fromkeys(range(len(graph.scenario)))
    max_path = dict.fromkeys(range(len(graph.scenario)))
    for scenario in min_path.keys():
        min_path[scenario] = 0
        real_path[scenario] = 0
        max_path[scenario] = 0
        for start, stop in pairwise(path_in_nodes):
            min_path[scenario] += graph.scenario[scenario][hash_nodes(start, stop)].min_length
            real_path[scenario] += graph.scenario[scenario][hash_nodes(start, stop)].length
            max_path[scenario] += graph.scenario[scenario][hash_nodes(start, stop)].max_length
    return min_path, real_path, max_path


class RegretSolver:
    def __init__(self, graph: "NDGraph", start: "NDNode", end: "NDNode"):
        self.graph = graph
        self.nxgraph = nx.Graph()
        for edge in self.graph.edges.values():
            self.nxgraph.add_edge(edge.source.name, edge.target.name)
        self.start_node = start
        self.end_node = end
        assert start.name in graph.nodes
        assert end.name in graph.nodes

    def get_estimated_minimum(self):
        # czas ucieka, poratuje sie nx'em żeby znaleźć ścieżki. niech mnie ławryn ma w opiece 🙏

        n = [
            min((i.min_length for i in self.graph.scenario[scenario].values()))
            for scenario in range(len(self.graph.scenario))
        ]
        j = nx.shortest_path_length(self.nxgraph, self.start_node.name, self.end_node.name)
        return [i * j for i in n], j

    def get_paths(self, max_len=None):
        if max_len:
            max_len = math.ceil(max_len * 1.1)
        for item in nx.all_simple_paths(self.nxgraph, self.start_node.name, self.end_node.name, cutoff=max_len):
            yield item
