from itertools import permutations

import salesman.solver.solver as s
from salesman.solver.graph import NDGraph, NDNode

# graph = NDGraph.watts_strogatz(10, 1, 1, 2)
# w_start = graph.nodes["0"]
# w_end   = graph.nodes["5"]
# solver = s.RegretSolver(graph, w_start, w_end)

graph = NDGraph()
w0 = NDNode(0)
w1 = NDNode(1)
w2 = NDNode(2)
w3 = NDNode(3)
w4 = NDNode(4)
w5 = NDNode(5)
w6 = NDNode(6)

graph.add_edge(w0, w1, possible_lengths=(20, 50))
graph.add_edge(w0, w2, possible_lengths=(12, 400))
graph.add_edge(w0, w3, possible_lengths=(13, 200))
graph.add_edge(w0, w4, possible_lengths=(14, 20))
graph.add_edge(w0, w5, possible_lengths=(15, 20))
graph.add_edge(w1, w6, possible_lengths=(10, 200))
graph.add_edge(w2, w6, possible_lengths=(10, 2002))
graph.add_edge(w3, w6, possible_lengths=(10, 23))
graph.add_edge(w4, w6, possible_lengths=(10, 24))
graph.add_edge(w5, w6, possible_lengths=(10, 25))
solver = s.RegretSolver(graph, w0, w6)

# scenarios = tuple(x for y in solver.get_paths() for x in solver.get_path_scenarios(y))

# for current_path in solver.get_shortest_paths():
#     val = max(
#         [
#             (sum(path_scenario) - sum(scenario_y))
#             for path_scenario, scenario_y in permutations(solver.get_path_scenarios(current_path), 2)
#         ]
#     )
#     if val < min_regret:
#         min_regret = val
#         print(f"New best regret = {min_regret}, path = {current_path}")

min_value = 1e10
best_path = None

scenarios = tuple(solver.generate_random_scenarios())
# scenarios = tuple(solver.get_all_scenarios())
# print(solver.sa_get_shortest_path(scenarios[0]))
# x = solver.generate_random_path(solver.start_node, solver.end_node, set())

# exit(-1)

for path_A, path_B in permutations(solver.get_shortest_paths(), 2):
    max_regret = -1e10
    path = None
    for scenario in scenarios:
        path_A_mapped_sum = sum([scenario[solver.edges_bimap[i]] for i in path_A])
        path_B_mapped_sum = sum([scenario[solver.edges_bimap[i]] for i in path_B])

        regret = path_A_mapped_sum - path_B_mapped_sum

        if regret > max_regret:
            max_regret = regret
            path = path_A

    if min_value > max_regret:
        print("found best solution", max_regret)
        min_value = max_regret
        best_path = path

# print(best_path)
# print(min_value)
