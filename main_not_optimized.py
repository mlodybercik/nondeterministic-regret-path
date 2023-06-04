from itertools import permutations

import salesman.solver.solver as s
from salesman.solver.graph import NDGraph

graph = NDGraph.watts_strogatz(10, 1, 1, 2)
w_start = graph.nodes["0"]
w_end = graph.nodes["5"]
solver = s.RegretSolver(graph, w_start, w_end)

min_regret = 1e10
best_path = []
for current_path in solver.get_paths():
    val = max(
        (
            sum(path_scenario) - sum(scenario_y)
            for path_scenario, scenario_y in permutations(solver.get_path_scenarios(current_path), 2)
        )
    )
    if val < min_regret:
        print(f"New best regret = {val}, path = {current_path}")
        min_regret = val
        best_path = current_path

print(f"Path regret min/max = {sum([i.min_length for i in best_path])}/{sum([i.max_length for i in best_path])}")

best_scenario = [0] * len(solver.graph.edges.values())
for edge in solver.graph.edges.values():
    best_scenario[solver.edges_bimap[edge]] = edge.min_length

best_path = solver.get_shortest_path(best_scenario)
print(f"Path normal min/max = {sum([i.min_length for i in best_path])}/{sum([i.max_length for i in best_path])}")

print("Small done")

graph = NDGraph.watts_strogatz(40, 1, 1, 5)
w_start = graph.nodes["0"]
w_end = graph.nodes["20"]
solver = s.RegretSolver(graph, w_start, w_end)

random_scenarios = tuple(solver.generate_random_scenarios())
random_paths = tuple(solver.get_shortest_path(scenario) for scenario in random_scenarios)


def calculate(path, scenario):
    return sum([scenario[solver.edges_bimap[edge]] for edge in path])


min_regret = 1e10
best_path = []
for current_path in random_paths:
    val = max(
        (
            calculate(current_path, path_scenario) - calculate(current_path, scenario_y)
            for path_scenario, scenario_y in permutations(random_scenarios, 2)
        )
    )
    if val < min_regret:
        print(f"New best regret = {val}, path = {current_path}")
        min_regret = val
        best_path = current_path

best_scenario = [0] * len(solver.graph.edges.values())
for edge in solver.graph.edges.values():
    best_scenario[solver.edges_bimap[edge]] = edge.min_length

print(f"Path regret min/max = {sum([i.min_length for i in best_path])}/{sum([i.max_length for i in best_path])}")

best_path = solver.get_shortest_path(best_scenario)
print(f"Path normal min/max = {sum([i.min_length for i in best_path])}/{sum([i.max_length for i in best_path])}")
