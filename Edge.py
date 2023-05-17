class Edge:
    def __init__(self, capacity, flow =0, cost = 1):
        self._capacity = capacity  # Capacity of the edge
        self.flow = flow  # Flow of the edge
        self._cost = cost  # Distance or cost of the edge


    def get_residual_capacity(self):
        return self._capacity - self.flow

    def get_flow(self):
        return self.flow

    def set_flow(self, flow):
        self.flow = flow

    def get_capacity(self):
        return self._capacity

    def get_cost(self):
        return self._cost

    def set_cost(self, cost):
        self._cost = cost
