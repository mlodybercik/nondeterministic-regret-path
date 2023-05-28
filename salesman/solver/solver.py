import random
import typing as T

from . import logger

if T.TYPE_CHECKING:
    from .graph import NDEdge, NDGraph, NDNode


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

    def iterator(self):
        # min ( max { f(x, s) - f*(s) } )
        #  x    s∈S     ^decyzja ^oszacowanie
        # w naszym przypadku będzie to różnica między wartością minimalną dla ścieżki a możliwym maksimum

        # w przypadku min-maxu zwykłego szukamy:
        # min max f(x, s)
        #  x  s∈S
        # gdzie szukamy samej najkrótszej możliwe ścieżki
        while True:
            path = generate_random_path(self.graph, self.start_node, self.end_node)
            min_path = sum([edge.min_length for edge in path])
            max_path = sum([edge.max_length for edge in path])
            real_path = sum([edge.length for edge in path])

            logger.debug(
                f"Found path iters |{len(path)}|, ||{real_path:.2f}||, ||{min_path:.2f}||min, ||{max_path:.2f}||max"
            )
            yield path, max_path - min_path + real_path
