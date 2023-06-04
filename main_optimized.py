import time

import salesman.solver.solver as s
from salesman.solver.graph import NDGraph


def get_min_of_path(path):
    return sum([i.min_length for i in path])


def get_max_of_path(path):
    return sum([i.max_length for i in path])


def calculate_normal(solver: s.RegretSolver):
    start = time.perf_counter()
    # szukanie najkrótszej ścieżki po kryterium minimum
    best_scenario = [0] * len(solver.graph.edges.values())
    for edge in solver.graph.edges.values():
        best_scenario[solver.edges_bimap[edge]] = edge.min_length
    best_path = solver.get_shortest_path(best_scenario)
    delta_min = time.perf_counter() - start
    best_max = get_max_of_path(best_path)
    best_min = get_min_of_path(best_path)
    # print(f"Path normal min min/max = {best_min}/{best_max}, took {delta_min}")

    # szukanie najkrtószej scieżki po kryterium maksimum
    start = time.perf_counter()
    worst_scenario = [0] * len(solver.graph.edges.values())
    for edge in solver.graph.edges.values():
        worst_scenario[solver.edges_bimap[edge]] = edge.max_length
    worst_path = solver.get_shortest_path(worst_scenario)
    delta_max = time.perf_counter() - start
    worst_max = get_max_of_path(worst_path)
    worst_min = get_min_of_path(worst_path)
    # print(f"Path normal max min/max = {worst_min}/{worst_max}, took {delta_max}")

    # szukanie najkrtószej scieżki po kryterium maksimum
    start = time.perf_counter()
    mean_scenario = [0] * len(solver.graph.edges.values())
    for edge in solver.graph.edges.values():
        mean_scenario[solver.edges_bimap[edge]] = sum(edge.possible_length) / 2
    mean_path = solver.get_shortest_path(mean_scenario)
    delta_mean = time.perf_counter() - start
    mean_max = get_max_of_path(mean_path)
    mean_min = get_min_of_path(mean_path)
    # print(f"Path normal mean min/max = {mean_min}/{mean_max}, took {delta_mean}")
    # fmt: off
    return (
        best_min, best_max, delta_min,
        worst_min, worst_max, delta_max,
        mean_min, mean_max, delta_mean
    )
    # fmt: on


def get_small_done(size: int):
    graph = NDGraph.watts_strogatz(size, 1, 1, 2)
    w_start = graph.nodes["0"]
    w_end = graph.nodes[f"{size//2}"]
    solver = s.RegretSolver(graph, w_start, w_end)

    start = time.perf_counter()
    shortest_paths = solver.get_shortest_paths()
    min_regret = 1e10
    best_path_regret = []
    for path_A in shortest_paths:
        max_regret = -1e10
        max_path = None
        worst_case_path_A = sum(solver.get_worst_scenario(path_A))
        for path_B in shortest_paths:
            best_case_path_B = sum(solver.get_best_scenario(path_B))
            val = worst_case_path_A - best_case_path_B

            if val > max_regret:
                # print(f"New semi-best regret = {val}")
                max_regret = val
                max_path = path_B

        if max_regret < min_regret:
            # print(f"New best regret = {max_regret}, path = {max_path}")
            min_regret = max_regret
            best_path_regret = max_path

    delta_regret = time.perf_counter() - start

    regret_max = get_max_of_path(best_path_regret)
    regret_min = get_min_of_path(best_path_regret)
    # print(f"Path regret min/max = {regret_min}/{regret_max}, took {delta_regret}")
    # fmt: off
    return (
        regret_min, regret_max, delta_regret,
        *calculate_normal(solver)
    )
    # fmt: on


def get_big_done(size: int):
    graph = NDGraph.watts_strogatz(size, 1, 5, 5)
    w_start = graph.nodes["0"]
    w_end = graph.nodes[f"{size//2}"]
    solver = s.RegretSolver(graph, w_start, w_end)

    start = time.perf_counter()

    random_scenarios = tuple(solver.generate_random_scenarios())
    random_paths = tuple(solver.get_shortest_path(scenario) for scenario in random_scenarios)

    min_regret = 1e10
    best_path_regret = []
    for path_A in random_paths:
        max_regret = -1e10
        max_path = None
        worst_case_path_A = sum(solver.get_worst_scenario(path_A))
        for path_B in random_paths:
            best_case_path_B = sum(solver.get_best_scenario(path_B))
            val = worst_case_path_A - best_case_path_B

            if val > max_regret:
                # print(f"New semi-best regret = {val}")
                max_regret = val
                max_path = path_A

        if max_regret < min_regret:
            # print(f"New best regret = {max_regret}, path = {max_path}")
            min_regret = max_regret
            best_path_regret = max_path

    best_scenario = [0] * len(solver.graph.edges.values())
    for edge in solver.graph.edges.values():
        best_scenario[solver.edges_bimap[edge]] = edge.min_length

    delta_regret = time.perf_counter() - start

    regret_max = get_max_of_path(best_path_regret)
    regret_min = get_min_of_path(best_path_regret)
    # print(f"Path regret min/max = {regret_min}/{regret_max}")

    return (regret_min, regret_max, delta_regret, *calculate_normal(solver))


def round_m(a):
    return [round(i, 2) for i in a]


print(10, round_m(get_small_done(10)))
print(12, round_m(get_small_done(12)))
print(14, round_m(get_small_done(14)))
print(16, round_m(get_small_done(16)))
print(18, round_m(get_small_done(18)))
print(20, round_m(get_small_done(20)))

print(50, round_m(get_big_done(50)))
print(70, round_m(get_big_done(70)))
print(90, round_m(get_big_done(90)))
print(110, round_m(get_big_done(110)))
print(130, round_m(get_big_done(130)))
print(150, round_m(get_big_done(150)))
