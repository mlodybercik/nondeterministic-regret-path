import csv

import salesman.solver.solver as s
from salesman.solver.graph import NDGraph

graph = NDGraph.watts_strogatz(1000, 1, 1, 450)
g0 = graph.nodes["0"]
g50 = graph.nodes["500"]
solver = s.RegretSolver(graph, g0, g50)
print("estimating minimum")
_, n = solver.get_estimated_minimum()
path_generator = solver.get_paths(n)

global_minimum = 1e10

minmax_min = 1e10
minmax_max = 1e10
minmax_mean = 1e10

minmax_min_path = None
minmax_max_path = None
minmax_mean_path = None

regret_min = 1e10
regret_max = 1e10
regret_mean = 1e10

regret_min_path = None
regret_max_path = None
regret_mean_path = None

with open("temp/resp.csv", "w") as file:
    writer = csv.writer(file, "excel")
    writer.writerow(
        ["minmax_min", "minmax_max", "minmax_mean", "regret_min", "regret_max", "regret_mean", "global_minimum"]
    )

    for i in range(500):
        print(i, end="\r")
        path = next(path_generator)
        min_path, max_path = s.calculate_single(path)

        if global_minimum > min_path:
            global_minimum = min_path

        if minmax_min > min_path:
            print("Found new minmax_min")
            minmax_min = min_path
            minmax_min_path = path

        if minmax_max > max_path:
            print("Found new minmax_max")
            minmax_max = max_path
            minmax_max_path = path

        if minmax_mean > (mean_path := ((min_path + max_path) / 2)):
            print("Found new minmax_mean")
            minmax_mean = mean_path
            minmax_mean_path = path

        temp_regret_min = min_path - global_minimum
        temp_regret_max = max_path - global_minimum
        temp_regret_mean = mean_path - global_minimum

        if regret_min >= temp_regret_min:
            print("Found new regret_min")
            regret_min = temp_regret_min
            regret_min_path = path

        if regret_max >= temp_regret_max:
            print("Found new regret_max")
            regret_max = temp_regret_max
            regret_max_path = path

        if regret_mean >= temp_regret_mean:
            print("Found new regret_mean")
            regret_mean = temp_regret_mean
            regret_mean_path = path

        writer.writerow(
            (
                s.real_path(minmax_min_path),
                s.real_path(minmax_max_path),
                s.real_path(minmax_mean_path),
                s.real_path(regret_min_path),
                s.real_path(regret_max_path),
                s.real_path(regret_mean_path),
                global_minimum,
            )
        )
        file.flush()

print(f"minmax_min {s.real_path(minmax_min_path)}")
print(f"minmax_max {s.real_path(minmax_max_path)}")
print(f"minmax_mean {s.real_path(minmax_mean_path)}")

print(f"regret_min_path {s.real_path(regret_min_path)}")
print(f"regret_max_path {s.real_path(regret_max_path)}")
print(f"regret_mean_path {s.real_path(regret_mean_path)}")
