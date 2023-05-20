from collections import deque

from flow_solvers.Flow_graph import Flow_graph
from flow_solvers import INFINITY

class FF_solver(Flow_graph):
    def __init__(self, num_nodes, s, t, use_bfs=False):
        super().__init__(num_nodes, s, t)
        self.visitedToken = 1
        self.visited = [0] * self.num_nodes
        self.use_bfs = use_bfs

    def solve_max_flow(self):
        if self.use_bfs:
            find_aug_path_method = self.bfs_edmonds_karp
        else:
            find_aug_path_method = self.dfs_classic_ff
        path = find_aug_path_method(self.source, INFINITY)
        while path is not None:
            self.max_flow += self.augment_path(path)
            self.visitedToken += 1
            path = find_aug_path_method(self.source, INFINITY)


    def dfs_classic_ff(self, node, flow):
        if node == self.sink:
            return []

        stack = [(node, flow, [])]  # Stack to track current node, current flow, and the path
        while stack:
            curr_node, curr_flow, path = stack.pop()  # Get the current node, current flow, and path from the stack
            self.visited[curr_node] = self.visitedToken  # Mark the current node as visited
            for edge in self.get_outgoing_edges(curr_node):  # Iterate through outgoing edges from the current node
                is_unvisited_node = self.visited[edge.node_j] != self.visitedToken
                if edge.is_rem_capacity_positive() and is_unvisited_node:
                    new_flow = min(curr_flow, edge.remaining_capacity())  # Calculate the new flow
                    new_path = path + [edge]  # Update the path by adding the current edge
                    if edge.node_j == self.sink:  # If the sink node is reached, return the augmented path
                        return new_path
                    stack.append((edge.node_j, new_flow, new_path))  # Push the next node, new flow, and new path to the stack
        return None  # If no augmenting path is found, return None

    def bfs_edmonds_karp(self, node, flow):
        if node == self.sink:
            return []
        self.visited[node] = self.visitedToken
        q = deque([(node, [])])  # Queue to track current node and path
        while q:
            curr_node, path = q.popleft()  # Get the current node and path from the front of the queue
            for edge in self.get_outgoing_edges(curr_node):  # Iterate through outgoing edges from the current node
                is_unvisited_node = self.visited[edge.node_j] != self.visitedToken
                if edge.is_rem_capacity_positive() and is_unvisited_node:
                    new_flow = min(flow, edge.remaining_capacity())  # Calculate the new flow
                    new_path = path + [edge]  # Update the path by adding the current edge
                    if edge.node_j == self.sink:  # If the sink node is reached, return the augmented path
                        return new_path
                    self.visited[edge.node_j] = self.visitedToken  # Mark the current node as visited
                    q.append((edge.node_j, new_path))  # Enqueue the next node and new path

        return None  # If no augmenting path is found, return None
