import os
import time
import matplotlib.pyplot as plt
import statistics
from chemin_augmentant import parse_file
from flow_solvers.Dinitz_solver import Dinitz_solver
from flow_solvers.FF_solver import FF_solver


def measure_resolution_time(flow_graph):
    start_time = time.time()
    max_flow = flow_graph.get_max_flow()
    end_time = time.time()
    resolution_time = end_time - start_time
    return resolution_time
def process_instances():
    for n in range(1,15):
        results = []
        for nodes in range(100, 1600, 100):
            for density in range(1, 4):
                instance = f"inst-{nodes}-0.{density}.txt"
                file_path = os.path.join(directory, instance)
                flow_graph = parse_file(file_path)
                resolution_time = measure_resolution_time(flow_graph)
                results.append(resolution_time)
        export_results(results,n)

def export_results(results,n):
    with open("resPython"+str(n)+".txt", "w") as file:
        for result in results:
            file.write(str(result)+"\n")
directory = "Instances"
results = process_instances()
