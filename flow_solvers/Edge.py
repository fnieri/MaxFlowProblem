class Edge:
    def __init__(self, from_node_i: int, to_node_j: int, capacity: int, flow: int = 0, residual_edge = None):
        self.node_i = from_node_i
        self.node_j = to_node_j
        self.capacity = capacity
        self.flow = flow
        self.residual_edge = residual_edge

    def is_residual(self):
        return self.capacity == 0

    def remaining_capacity(self):
        return self.capacity - self.flow

    def augment(self, bottleneck):
        self.flow += bottleneck
        self.residual_edge.flow -= bottleneck


    def is_rem_capacity_positive(self):
        return self.remaining_capacity() > 0