import csv

import salesman.solver.solver as s
from salesman.solver.graph import NDGraph

graph = NDGraph.watts_strogatz(1000, 1, 1, 300)
g0 = graph.nodes["0"]
g50 = graph.nodes["50"]
solver = s.RegretSolver(graph, g0, g50)

graph.create_scenario()
graph.create_scenario()

minmax_min = 1e10
minmax_min_path = None
minmax_max = 1e10
minmax_max_path = None
minmax_mean = 1e10
minmax_mean_path = None

regret_min = 1e10
regret_min_path = None
regret_max = 1e10
regret_max_path = None
regret_mean = 1e10
regret_mean_path = None

print("estimating minimum")
global_minimum, n = solver.get_estimated_minimum()
print(global_minimum, n)
path_generator = solver.get_paths(n)

headers = []
for scenario in range(len(graph.scenario)):
    headers.extend((f"min_{scenario}", f"max_{scenario}", f"real_{scenario}"))
headers.extend(("f_value", "length", "iter"))

items = ["min", "max", "mean", "regret_min", "regret_max", "regret_mean"]
files = {}
writers = {}

for item in items:
    files[item] = open(f"temp/{item}.csv", "w")
    writers[item] = csv.DictWriter(files[item], headers, dialect="excel", lineterminator="\n")


for iter, path in enumerate(path_generator):
    print(iter, end="\r")
    min_path, real_path, max_path = s.calculate_path(graph, path)

    min_path_sum = sum(min_path.values())
    max_path_sum = sum(max_path.values())
    mean_path_sum = (min_path_sum + max_path_sum) / 2
    real_path_sum = sum(real_path.values())

    if minmax_min > min_path_sum:
        print("Found new minmax_min")
        minmax_min = min_path_sum

        save = {}
        for key in min_path.keys():
            save[f"min_{key}"] = min_path[key]
            save[f"real_{key}"] = real_path[key]
            save[f"max_{key}"] = max_path[key]

        save["f_value"] = min_path_sum
        save["length"] = len(path)
        save["iter"] = iter
        writers["min"].writerow(save)

    if minmax_max > max_path_sum:
        print("Found new minmax_max")
        minmax_max = max_path_sum

        save = {}
        for key in min_path.keys():
            save[f"min_{key}"] = min_path[key]
            save[f"real_{key}"] = real_path[key]
            save[f"max_{key}"] = max_path[key]

        save["f_value"] = max_path_sum
        save["length"] = len(path)
        save["iter"] = iter
        writers["max"].writerow(save)

    if minmax_mean > mean_path_sum:
        print("Found new minmax_mean")
        minmax_mean = mean_path_sum

        save = {}
        for key in min_path.keys():
            save[f"min_{key}"] = min_path[key]
            save[f"real_{key}"] = real_path[key]
            save[f"max_{key}"] = max_path[key]

        save["f_value"] = mean_path_sum
        save["length"] = len(path)
        save["iter"] = iter
        writers["mean"].writerow(save)

    temp_regret_min = sum([min_path[i] - global_minimum[i] for i in range(len(min_path))])
    temp_regret_max = sum([max_path[i] - global_minimum[i] for i in range(len(min_path))])
    temp_regret_mean = sum([min_path[i] - global_minimum[i] for i in range(len(min_path))])

    if regret_min > temp_regret_min:
        print("Found new regret_min")
        regret_min = temp_regret_min

        save = {}
        for key in min_path.keys():
            save[f"min_{key}"] = min_path[key]
            save[f"real_{key}"] = real_path[key]
            save[f"max_{key}"] = max_path[key]

        save["f_value"] = temp_regret_min
        save["length"] = len(path)
        save["iter"] = iter
        writers["regret_min"].writerow(save)

    if regret_max >= temp_regret_max:
        print("Found new regret_max")
        regret_max = temp_regret_max
        save = {}
        for key in min_path.keys():
            save[f"min_{key}"] = min_path[key]
            save[f"real_{key}"] = real_path[key]
            save[f"max_{key}"] = max_path[key]

        save["f_value"] = temp_regret_max
        save["length"] = len(path)
        save["iter"] = iter
        writers["regret_max"].writerow(save)

    if regret_mean >= temp_regret_mean:
        print("Found new regret_mean")
        regret_mean = temp_regret_mean
        save = {}
        for key in min_path.keys():
            save[f"min_{key}"] = min_path[key]
            save[f"real_{key}"] = real_path[key]
            save[f"max_{key}"] = max_path[key]

        save["f_value"] = temp_regret_mean
        save["length"] = len(path)
        save["iter"] = iter
        writers["regret_mean"].writerow(save)
