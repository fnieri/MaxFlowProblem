from DirectedFlowGraph import DirectedFlowGraph as DFGraph

class ResidualFlowGraph(DFGraph):
    def __init__(self,DFG):
        self.DFG = DFG
        super().__init__(DFG.num_nodes)
        self.init_residual_edges()

    def init_residual_edges(self):
        for i, j in self.DFG.source_target_to_edge.keys():
            edge = self.DFG.get_edge(i, j)
            edge_residual_capacity = edge.get_residual_capacity()
            edge_flow = edge.get_flow()
            potential_diff = self._calc_potential_difference(i,j)
            edge_cost = edge.get_cost()
            if (0<edge_residual_capacity):
                reduced_cost = edge_cost + potential_diff
                self.add_edge(i, j, edge_residual_capacity, reduced_cost)
            if(edge_flow>0):
                reduced_cost = -edge_cost - potential_diff
                self.add_edge(j, i, edge_flow,reduced_cost)

    def _calc_potential_difference(self, i, j):
        w_i, w_j = self._get_potential_from_DFG(i), self._get_potential_from_DFG(j)
        return -w_i + w_j

    def _get_potential_from_DFG(self,node):
        return self.DFG.get_potential(node)






