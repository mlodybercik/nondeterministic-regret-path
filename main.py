import salesman

window = salesman.Window((900, 900), "siema eniu")
window.graph = salesman.NDGraph.watts_strogatz(15, 0.75, 10)

window.loop()
