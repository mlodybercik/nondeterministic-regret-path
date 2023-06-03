import typing as T
from itertools import tee

import networkx as nx
import numpy as np

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


V = T.TypeVar("V")


def pairwise(iterable: T.Sequence[V]) -> T.Iterator[T.Tuple[V, V]]:
    # pairwise('ABCDEFG') --> AB BC CD DE EF FG
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def get_possible_neighbours(neighbour_connections: T.Sequence["NDEdge"], visited: T.Sequence["NDNode"]):
    return [
        connection
        for connection in neighbour_connections
        if connection.source not in visited or connection.target not in visited
    ]


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

    def nodes_to_path(self, path: T.Sequence["NDNode"]):
        return [self.graph.edges[hash_nodes(x, y)] for x, y in pairwise(path)]

    def path_to_nodes(self, path: T.Sequence["NDEdge"]):
        ret: T.Sequence["NDNode"] = []
        for edge, next_edge in pairwise(path):
            if edge.source in next_edge:
                ret.append(edge.target)
            else:
                ret.append(edge.source)
        if edge.source == ret[-1]:
            ret.append(edge.target)
            if edge.target == next_edge.source:
                ret.append(next_edge.target)
            else:
                ret.append(next_edge.source)
        else:
            ret.append(edge.source)
            if edge.source == next_edge.target:
                ret.append(next_edge.source)
            else:
                ret.append(next_edge.target)
        return ret

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

    def generate_random_scenarios(self):
        n_edges = len(self.graph.edges)
        possibilities = (0, 1)
        max_to_generate = round(np.power(n_edges, 4 / 5))

        for i_scenario in range(max_to_generate):
            yield tuple(
                self.edges_bimap[i].possible_length[mask]
                for i, mask in enumerate(np.random.choice(possibilities, n_edges))
            )

    def sa_get_shortest_path(self, scenario: T.Sequence[int], iterations: int = 1000):
        def schedule(k=20, lam=0.005):
            return lambda t: (k * np.exp(-lam * t) if t < iterations else 0)

        def path_length(path: T.Sequence["NDEdge"]):
            return sum([scenario[self.edges_bimap[i]] for i in path])

        def generate_similiar(path: T.Sequence["NDEdge"]):
            return self.sa_generate_similar_path(path)

        current = self.generate_random_path(self.start_node, self.end_node, set())
        scheduler = schedule()

        for i in range(iterations):
            temperature = scheduler(i)
            new = generate_similiar(current)
            length_delta = path_length(new) - path_length(current)
            if length_delta < 0 or (np.random.random() > (np.exp(-1 * length_delta / temperature))):
                current = new
        return current

    def generate_random_path(
        self, start: "NDNode", end: "NDNode", visited: T.Set["NDNode"] = set()
    ) -> T.Sequence["NDNode"]:
        done = False
        path = []
        i = 0
        while not done:
            if i > 10:
                raise KeyError("no solutions found")
            current_node = start
            path: T.Sequence["NDEdge"] = []
            curr_visited = set(visited)
            curr_visited.add(start)

            while len((connections := get_possible_neighbours(self.graph.get_edges_of(current_node), curr_visited))):
                current_connection = np.random.choice(connections)
                current_node = (
                    current_connection.source
                    if current_node != current_connection.source
                    else current_connection.target
                )
                path.append(current_connection)
                curr_visited.add(current_node)
                if current_node == end:
                    done = True
                    break
            i += 1
        return path

    def sa_generate_similar_path(self, path: T.Sequence["NDEdge"]):
        subpath_start, subpath_end = sorted(np.random.choice(len(path) - 1, 2, False))
        try:
            path_to_node = self.path_to_nodes(path)
            insert_path = self.generate_random_path(
                path_to_node[subpath_start], path_to_node[subpath_end], set(path_to_node[:subpath_start])
            )
        except KeyError:
            return path
        return self.nodes_to_path(path_to_node[:subpath_start] + insert_path + path_to_node[subpath_end:])
