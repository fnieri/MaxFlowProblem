import argparse

from flow_solvers.Dinitz_solver import *
import time

def solve_instance(instance_path):
    dSolver = parse_file(instance_path)
    try:
        n,p = instance_path[:-4].split("-")[1:]
    except:
        print("Error parsing instance name, make sure the instance is located in the same directory as this script")
        print("Please make sure the package flow_solvers is also present in the same directory")
        print("The instance name should be of the form: inst-n-p.txt")
        return None
    print("Solving instance: ", instance_path)
    t = time.time()
    print("Max Flow: ", dSolver.get_max_flow())
    print("Time taken: ", time.time()-t)
    print("is optimal: ", dSolver.identify_min_cut()==dSolver.get_max_flow())
    dSolver.export_graph("model-"+n+"-"+p+".path")

def parse_file(instance_path):
    try:
        with open(instance_path, 'r') as file:
            lines = file.readlines()
            num_nodes = int(lines[0].split()[1])
            s = int(lines[1].split()[1])
            t = int(lines[2].split()[1])
            dSolver = Dinitz_solver(num_nodes, s, t)
            for line in lines[4:]:
                try:
                    source, target, capacity = map(int, line.split())
                    dSolver.add_edge(source, target, capacity)
                except ValueError:
                    print("Error parsing line: " + line)
            return dSolver
    except FileNotFoundError:
        print("File not found: " + instance_path)
        print("Please make sure the instance is found in the directory of this script, or provide the full path to the instance")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('instance_path', help='Path to the instance file')
    args = parser.parse_args()
    instance_path = args.instance_path
    solve_instance(instance_path)