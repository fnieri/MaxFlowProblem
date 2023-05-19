from abc import ABC, abstractmethod
from flow_solvers.Edge import Edge

class Flow_graph(ABC):
    def __init__(self, num_nodes, source, sink, ):
        self.num_nodes = num_nodes
        self.source = source
        self.sink = sink
        self.adj_list = [[] for _ in range(self.num_nodes)]  # List of edges for each node
        self.solved = False
        self.max_flow = 0


    def add_edge(self, node_i: int, node_j: int, capacity: int):
        if(capacity<=0):
            raise ValueError("Forward edge capacity <= 0")
        e1 = Edge(node_i, node_j, capacity)
        e2 = Edge(node_j, node_i, 0)
        e1.residual_edge = e2
        e2.residual_edge = e1
        self.get_outgoing_edges(node_i).append(e1)
        self.get_outgoing_edges(node_j).append(e2)

    def print_graph(self):
        print("Graph:")
        print("node_i, node_j, capacity, flow")
        i = 0
        for node in self.get_adj_list():
            for edge in node:
                i += 1
                print(edge.node_i, edge.node_j, edge.capacity)

    def get_outgoing_edges(self, node: int) -> list[Edge]:
        return self.adj_list[node]

    def get_adj_list(self):
        return self.adj_list

    def get_max_flow(self):
        self.solve()
        return self.max_flow

    def solve(self):
        if(self.solved):
            return
        self.solved = True
        self.solve_max_flow()

    def augment_path(self, path):
        bottleneck = min(edge.remaining_capacity() for edge in path)
        for edge in path:
            edge.augment(bottleneck)
        return bottleneck

    @abstractmethod
    def solve_max_flow(self):
        pass


