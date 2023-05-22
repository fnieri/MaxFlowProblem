from abc import ABC, abstractmethod
from collections import deque

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



    def get_outgoing_edges(self, node: int):
        return self.adj_list[node]

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
        self.max_flow+= bottleneck

    def identify_min_cut(self):
        # Perform BFS to compute reachable nodes from the source
        reachable = self._bfs_for_mincut()
        # Compute the minimum cut value
        min_cut_value = self._compute_min_cut_value(reachable)

        return min_cut_value

    def _bfs_for_mincut(self):
        # Perform BFS to compute reachable nodes from the source
        visited = [False] * self.num_nodes
        q = deque()
        q.append(self.source)
        visited[self.source] = True
        while q:
            node = q.popleft()
            for edge in self.get_outgoing_edges(node):
                if edge.remaining_capacity() > 0 and not visited[edge.node_j]: # If there is capacity and the node has not been visited, ie: in the original graph and not in the residual graph
                    visited[edge.node_j] = True
                    q.append(edge.node_j)
        return visited

    def _compute_min_cut_value(self, reachable):
        min_cut_value = 0
        for node in range(self.num_nodes):
            for edge in self.get_outgoing_edges(node):
                if reachable[edge.node_i] and not reachable[edge.node_j]:
                    min_cut_value += edge.capacity
        return min_cut_value

    ## Printing and exporting
    def print_graph(self):
        print("Graph:")
        print("node_i, node_j, capacity, flow")
        i = 0
        for node in self.adj_list:
            for edge in node:
                i += 1
                print(edge.node_i, edge.node_j, edge.capacity, edge.flow)


    def export_graph(self, filename):
        with open(filename, 'w') as file:
            file.write("Max flow: {}\n".format(self.max_flow))
            file.write("Total nodes: {}\n".format(self.num_nodes))
            file.write("Source: {}\n".format(self.source))
            file.write("Sink: {}\n".format(self.sink))
            # Write headers
            file.write("{:<8}  {:<8}  {:<8}  {:<8}\n".format("node_i", "node_j", "capacity", "flow"))

            # Write edge information
            for node_i, edges in enumerate(self.adj_list):
                for edge in edges:
                    file.write("{:<8}  {:<8}  {:<8}  {:<8}\n".format(edge.node_i, edge.node_j, edge.capacity, edge.flow))
        print("Graph exported to {}".format(filename))



    @abstractmethod
    def solve_max_flow(self):
        pass


