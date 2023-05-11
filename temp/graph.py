import random

class Edge:
    def __init__(self, node1, node2, min_length, max_length):
        self.node1 = node1
        self.node2 = node2
        self.min_length = min_length
        self.max_length = max_length

    def get_length(self):
        return random.uniform(self.min_length, self.max_length)

class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = []
        self.connections = {}

    def add_node(self, node):
        self.nodes.add(node)
        self.connections[node] = []

    def add_edge(self, node1, node2, min_length, max_length):
        self.nodes.add(node1)
        self.nodes.add(node2)
        edge = Edge(node1, node2, min_length, max_length)
        self.edges.append(edge)
        self.connections[node1].append(node2)
        self.connections[node2].append(node1)

    def get_edges(self, node):
        return [edge for edge in self.edges if edge.node1 == node or edge.node2 == node]

    def get_neighbors(self, node):
        neighbors = []
        for edge in self.get_edges(node):
            if edge.node1 == node:
                neighbors.append(edge.node2)
            else:
                neighbors.append(edge.node1)
        return neighbors
    
if __name__ == '__main__':
    # test jak działa
    graph = Graph()
    graph.add_node("A")
    graph.add_node("B")
    graph.add_node("C")

    graph.add_edge("A", "B", 1, 3)
    graph.add_edge("B", "C", 2, 4)
    graph.add_edge("A", "C", 3, 5)

    print("Sąsiedzi A:", graph.get_neighbors("A"))

    for edge in graph.get_edges("A"):
        print(f"Długość krawędzi między {edge.node1} i {edge.node2}: {edge.get_length()}")

    print(graph.edges[0].node1)
    print(graph.connections)