from flow_solvers.Flow_graph import Flow_graph
from flow_solvers import INFINITY
from collections import deque
class Dinitz_solver(Flow_graph):
    def __init__(self, num_nodes, source, sink):
        super().__init__(num_nodes, source, sink)
        self.level = [0] * num_nodes

    def solve_max_flow(self):
        while self.bfs_phase():
            # next[i] gives the next edge index to index in the adjacency list for node i - Optimization by Even & Itai - Prunes dead ends as part of DFS
            # Reset every iteration to allow taking previously forbidden edges
            next = [0] * self.num_nodes
            # Find max flow by adding all augmenting path flows.
            path = self.dfs_phase(self.source, next)
            while path is not None:
                self.max_flow += self.augment_path(path)
                path = self.dfs_phase(self.source, next)

    # Computes the level of each node in the graph using BFS
    def bfs_phase(self):
        self.level = [-1] * self.num_nodes
        q = deque()
        q.append(self.source)
        self.level[self.source] = 0
        while q:
            curr_node = q.popleft()
            for edge in self.get_outgoing_edges(curr_node):
                is_unvisited_node = self.level[edge.node_j] == -1
                if edge.is_rem_capacity_positive() and is_unvisited_node:
                    self.level[edge.node_j] = self.level[curr_node] + 1
                    q.append(edge.node_j)
        # Return whether we were able to reach the sink node. If not, the graph is fully saturated, and we can stop performing max flow.
        return self.level[self.sink] != -1


    #Finds an augmenting path from source to sink using DFS
    def dfs_phase(self, curr_node, next, path=[]):
        if curr_node == self.sink:
            return path
        num_edges = len(self.get_outgoing_edges(curr_node))
        while next[curr_node] < num_edges:
            edge = self.get_outgoing_edges(curr_node)[next[curr_node]]
            is_progressive_edge = self.level[edge.node_j] == self.level[curr_node] + 1
            if edge.is_rem_capacity_positive() and is_progressive_edge:
                    result_path = self.dfs_phase(edge.node_j, next, path + [edge])
                    if result_path is not None:
                        return result_path
            next[curr_node] += 1
        return None



