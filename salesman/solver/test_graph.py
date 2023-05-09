import unittest

from .graph import NDEdge, NDGraph, NDNode


class TestGraph(unittest.TestCase):
    # sample graph
    #   B
    #  / \
    # A   D - E
    #  \ /
    #   C

    def test_graph_from_str(self):
        graph = NDGraph()

        graph.add_edge("A", "B", scale=10)
        graph.add_edge("A", "C", scale=10)
        graph.add_edge("B", "D", scale=10)
        graph.add_edge("C", "D", scale=10)
        graph.add_edge("D", "E", scale=10)

        nodeB = graph.nodes["B"]
        nodeC = graph.nodes["C"]
        nodeD = graph.nodes["D"]
        nodeE = graph.nodes["D"]

        neighbours = graph.get_neighbors("A")
        self.assertIn(nodeB, neighbours)
        self.assertIn(nodeC, neighbours)

        self.assertNotIn(nodeD, neighbours)
        self.assertNotIn(nodeE, neighbours)

    def test_graph_from_edges(self):
        graph = NDGraph()

        nodeA = NDNode("A")
        nodeB = NDNode("B")
        nodeC = NDNode("C")
        nodeD = NDNode("D")
        nodeE = NDNode("E")

        graph.add_from_edge(NDEdge.from_random(nodeA, nodeB, 10))
        graph.add_from_edge(NDEdge.from_random(nodeA, nodeC, 10))
        graph.add_from_edge(NDEdge.from_random(nodeB, nodeD, 10))
        graph.add_from_edge(NDEdge.from_random(nodeC, nodeD, 10))
        graph.add_from_edge(NDEdge.from_random(nodeD, nodeE, 10))

        neighbours = graph.get_neighbors(nodeA)
        self.assertIn(nodeB, neighbours)
        self.assertIn(nodeC, neighbours)

        self.assertNotIn(nodeD, neighbours)

    # def test_ws_model(self):
    #     graph = NDGraph.watts_strogatz(20, 0.5, 10)
    #     for edge in graph.edges:
    #         print(f"({edge.source.name}, {edge.target.name}),", end=" ")
