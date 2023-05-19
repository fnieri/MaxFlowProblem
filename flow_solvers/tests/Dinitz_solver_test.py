from flow_solvers.FF_solver import FF_solver
from flow_solvers.Dinitz_solver import Dinitz_solver

n = 11
s = n-1
t = n-2
solver = Dinitz_solver(n, s, t)
solver.add_edge(s, 0, 5)
solver.add_edge(s, 1, 10)
solver.add_edge(s, 2, 15)
solver.add_edge(0, 3, 10)
solver.add_edge(1, 0, 15)
solver.add_edge(1, 4, 20)
solver.add_edge(2, 5, 25)
solver.add_edge(3, 4, 25)
solver.add_edge(3, 6, 10)
solver.add_edge(4, 2, 5)
solver.add_edge(4, 7, 30)
solver.add_edge(5, 7, 20)
solver.add_edge(5, 8, 10)
solver.add_edge(7, 8, 15)

solver.add_edge(6, t, 5)
solver.add_edge(7, t, 15)
solver.add_edge(8, t, 10)
print("started")
solution = 30
print("Max Flow: ", solver.get_max_flow())
assert solver.get_max_flow() == solution, "Wrong answer, expected: " + str(solution)
print("Test passed")
print("is optimal: ", solver.identify_min_cut()==solver.get_max_flow())
flow_graph = Dinitz_solver(4, 0, 3)
flow_graph.add_edge(0, 1, 3)
flow_graph.add_edge(0, 2, 2)
flow_graph.add_edge(1, 2, 1)
flow_graph.add_edge(1, 3, 3)
flow_graph.add_edge(2, 3, 2)


print("Max Flow: ", flow_graph.get_max_flow())
print("is optimal: ", flow_graph.identify_min_cut()==flow_graph.get_max_flow())
flow_graph.export_graph("test_graph.path")