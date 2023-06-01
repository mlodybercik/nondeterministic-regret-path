import typing as T
from itertools import tee

import networkx as nx

from . import logger
from .graph import hash_nodes

if T.TYPE_CHECKING:
    from .graph import NDEdge, NDGraph, NDNode


class BidirectionalDict(dict):
    def __setitem__(self, key, val):
        dict.__setitem__(self, key, val)
        dict.__setitem__(self, val, key)

    def __delitem__(self, key):
        dict.__delitem__(self, self[key])
        dict.__delitem__(self, key)


def pairwise(iterable):
    # pairwise('ABCDEFG') --> AB BC CD DE EF FG
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


class RegretSolver:
    def __init__(self, graph: "NDGraph", start: "NDNode", end: "NDNode"):
        self.graph = graph
        self.nxgraph = nx.Graph()
        for edge in self.graph.edges.values():
            self.nxgraph.add_edge(edge.source, edge.target)
        self.start_node = start
        self.end_node = end

        self.edges_bimap = BidirectionalDict()
        for i, edge in enumerate(self.graph.edges.values()):
            self.edges_bimap[i] = edge

        assert start.name in graph.nodes
        assert end.name in graph.nodes

    def nodes_to_path(self, path: T.Sequence[int]):
        return [self.graph.edges[hash_nodes(x, y)] for x, y in pairwise(path)]

    def get_shortest_paths(self):
        for item in nx.all_shortest_paths(self.nxgraph, self.start_node, self.end_node):
            yield self.nodes_to_path(item)

    def get_paths(self):
        for item in nx.all_simple_paths(self.nxgraph, self.start_node, self.end_node):
            yield self.nodes_to_path(item)

    def get_all_scenarios(self):
        if len(self.graph.nodes) > 7:
            logger.warning("Ławryn mówił, że to może długo zająć D:")

        n_edges = len(self.graph.edges)

        for iteration in range(2**n_edges):
            yield tuple(self.edges_bimap[i].possible_length[bool(iteration & (2**i))] for i in range(n_edges))

    def get_path_scenarios(self, path: T.Sequence["NDEdge"]):
        path_length = len(path)

        for iteration in range(2**path_length):
            yield tuple(path[i].possible_length[~bool(iteration & (2**i))] for i in range(path_length))
