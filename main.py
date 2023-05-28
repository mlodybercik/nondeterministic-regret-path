import salesman

graph = salesman.NDGraph.watts_strogatz(20, 0.95, 30)
solver = salesman.RegretSolver(graph, graph.nodes["0"], graph.nodes["10"])

window = salesman.Window((900, 900), "siema eniu", solver)
window.graph = graph

window.loop()
