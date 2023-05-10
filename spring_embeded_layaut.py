import random
import math
from graph import Graph, Edge


def spring_embedder(graph : Graph, k=0.5, c=0.1, max_iterations=1000):
    dict_nodes = dict([*enumerate(graph.nodes)])
    n = len(dict_nodes)  
    # losowe położenia wierzchołków
    positions = {}
    for i in range(n):
        positions[i] = (random.random(), random.random())

    # pętla główna algorytmu
    for iteration in range(max_iterations):
        # obliczanie sił przyciągających między wierzchołkami połączonymi krawędzią
        forces = {}
        for i in range(n):
            forces[i] = [0, 0]
            for j in dict_nodes:
                dx = positions[j][0] - positions[i][0]
                dy = positions[j][1] - positions[i][1]
                distance = math.sqrt(dx*dx + dy*dy)
                force = k * (distance - 1) / (distance + 0.0001)
                forces[i][0] += force * dx
                forces[i][1] += force * dy

        # obliczanie sił odpychających między wierzchołkami
        for i in range(n):
            for j in range(i+1, n):
                dx = positions[j][0] - positions[i][0]
                dy = positions[j][1] - positions[i][1]
                distance = max(math.sqrt(dx*dx + dy*dy), 0.0001)  # zapobieganie dzieleniu przez zero
                force = c / (distance*distance)
                forces[i][0] -= force * dx
                forces[i][1] -= force * dy
                forces[j][0] += force * dx
                forces[j][1] += force * dy

        # aktualizacja położeń wierzchołków
        for i in range(n):
            positions[i] = (positions[i][0] + forces[i][0], positions[i][1] + forces[i][1])

    return {dict_nodes[i] :positions[i] for i in range(n)}


if __name__ == '__main__':
    # test jak działa
    graph = Graph()
    graph.add_node("A")
    graph.add_node("B")
    graph.add_node("C")

    graph.add_edge("A", "B", 1, 3)
    graph.add_edge("B", "C", 2, 4)
    graph.add_edge("A", "C", 3, 5)


    print(spring_embedder(graph))