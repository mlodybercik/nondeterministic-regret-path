import unittest

from .graph import NDGraph
from .solver import RegretSolver


class TestSolver(unittest.TestCase):
    # sample graph
    #   B - F
    #  / \   \
    # A   D - E
    #  \ /
    #   C

    def test_sample_path(self):
        graph = NDGraph()

        graph.add_edge("A", "B", scale=10)
        graph.add_edge("A", "C", scale=10)
        graph.add_edge("B", "D", scale=10)
        graph.add_edge("C", "D", scale=10)
        graph.add_edge("D", "E", scale=10)
        graph.add_edge("B", "F", scale=10)
        graph.add_edge("E", "F", scale=10)

        nodeA, nodeF = graph.nodes["A"], graph.nodes["F"]

        solver = RegretSolver(graph, nodeA, nodeF)
        self.assertTrue(next(solver.iterator()))

        solver = RegretSolver(graph, nodeF, nodeA)
        self.assertTrue(next(solver.iterator()))

    def test_sample_big_path(self):
        graph = NDGraph.watts_strogatz(30, 0.50, 10)
        solver = RegretSolver(graph, graph.nodes["0"], graph.nodes["15"])

        self.assertTrue(next(solver.iterator()))

    def test_generate_all_paths(self):
        graph = NDGraph.watts_strogatz(30, 0.50, 10)
        solver = RegretSolver(graph, graph.nodes["0"], graph.nodes["15"])

        print(next(solver.iterator()))
