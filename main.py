import salesman

graph = salesman.NDGraph.watts_strogatz(100, 0.95, 50)
solver = salesman.RegretSolver(graph, graph.nodes["0"], graph.nodes["50"])

window = salesman.Window((900, 900), "siema eniu", solver)
window.graph = graph

window.loop()
