import sys

from flow_solvers.Dinitz_solver import *

from time import time

from flow_solvers.FF_solver import FF_solver


def parse_file(file_path):
    with open(file_path, 'r') as file:
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

# dsolver = parse_file("instances/inst-1500-0.3.txt")

# print("done parsing")
# input()
# t1 = time()
# print(dsolver.get_max_flow())
# t2 = time()
# print(t2-t1)