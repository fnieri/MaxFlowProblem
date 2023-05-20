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
    return resolution_time, max_flow
def process_instances(directory, num_iterations):
    instances = os.listdir(directory)
    results = []
    nodes = 0
    edges = 0
    for instance in instances:
        file_path = os.path.join(directory, instance)
        y = get_instance_size(file_path)
        nodes += y[0]
        edges += y[1]
        # if instance[8] == "-":
        #     continue
        # for _ in range(num_iterations):
        #     file_path = os.path.join(directory, instance)
        #     flow_graph = parse_file(file_path)
        #     resolution_times = []
        #     max_flows = []
        #     resolution_time, max_flow = measure_resolution_time(flow_graph)
        #     results.append((file_path, resolution_time, max_flow))
    print(nodes/len(instances), edges/len(instances))
    return results



def analyze_results(results):
    # Separate the results by instance size
    size_results = {}
    for instance, resolution_time, max_flow in results:
        num_nodes, num_edges = get_instance_size(instance)  # Implement a function to extract the number of nodes and edges from the instance name
        size = (num_nodes, num_edges)
        if size not in size_results:
            size_results[size] = []
        size_results[size].append(resolution_time)

    # Calculate average resolution time and standard deviation for each instance size
    sizes = []
    avg_times = []
    std_devs = []
    for size, times in size_results.items():
        sizes.append(size)
        avg_time = statistics.mean(times)
        avg_times.append(avg_time)
        std_dev = statistics.stdev(times)
        std_devs.append(std_dev)

    # Sort the sizes in ascending order based on the number of nodes
    sizes.sort(key=lambda s: s[0])

    # Prepare labels for the x-axis
    x_labels = [f"Nodes: {size[0]}, Edges: {size[1]}" for size in sizes]

    # Plot the results
    plt.errorbar(range(len(sizes)), avg_times, yerr=std_devs, fmt='o-', label='Method X')  # Replace 'Method X' with the appropriate method name
    plt.xlabel('Instance Size')
    plt.ylabel('Resolution Time')
    plt.title('Resolution Time Comparison')
    plt.xticks(range(len(sizes)), x_labels, rotation=45)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def get_instance_size(instance):
    with open(instance, 'r') as file:
        lines = file.readlines()

    num_nodes = int(lines[0].split()[1])
    num_edges = int(lines[3].split()[1])

    return num_nodes, num_edges


directory = "Instances"
results = process_instances(directory,5)
analyze_results(results)
