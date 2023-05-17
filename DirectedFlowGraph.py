from Edge import Edge


class DirectedFlowGraph:
    def __init__(self, num_nodes):
        self.num_nodes = num_nodes  # Number of nodes in the graph
        self.adj_list = {node: set() for node in range(num_nodes)} # Adjacency list
        self.inverted_adj_list = {node: set() for node in range(num_nodes)} # Inverted adjacency list
        #maybe remove if not needed here, but in residual graph
        self.source_target_to_edge = {} # Dictionary mapping (source, target) to edge object
        self.potential_list = {node: 0 for node in range(num_nodes)}


    def add_edge(self, i, j, capacity, cost = 1):
        edge = Edge(capacity,0,cost)
        self.adj_list[i].add(j)  # Add outgoing edge to adj list
        self.inverted_adj_list[j].add(i)  # Add incoming edge to inverted adj list
        self.source_target_to_edge[(i, j)] = edge  # Add edge to dictionary

    def get_outgoing_neighbors(self, node):
        return self.adj_list[node]

    def get_incoming_neighbors(self, node):
        return self.inverted_adj_list[node]

#delete maybe
    def remove_edge(self, source, target):
        val = self.source_target_to_edge.pop((source, target), None)
        if val:
            self.adj_list[source].remove(target)
            self.inverted_adj_list[target].remove(source)
        return val

    def get_edge(self, source, target):
        return self.source_target_to_edge[(source, target)]

    def get_edge_cost(self, source, target):
        edge = self.get_edge(source, target)
        if edge is None:
            return None
        return edge.get_cost()

    def get_edge_capacity(self, source, target):
        edge = self.get_edge(source, target)
        if edge is None:
            return None
        return edge.get_capacity()

    def get_edge_flow(self, source, target):
        edge = self.get_edge(source, target)
        if edge is None:
            return None
        return edge.get_flow()

    def set_edge_flow(self, source, target, flow):
        edge = self.get_edge(source, target)
        if edge is None:
            return None
        edge.set_flow(flow)


    def get_residual_capacity(self, source, target):
        edge = self.get_edge(source, target)
        if edge is None:
            return None
        return edge.get_residual_capacity()

    def get_num_nodes(self):
        return self.num_nodes

    def print_graph_properties(self):
        print("Number of nodes:", self.num_nodes)
        for node in range(self.num_nodes):
            print("Node:", node)
            print("Potential:", self.potential_list[node])
            print("Outgoing neighbors:")
            for neighbor in self.adj_list[node]:
                edge = self.get_edge(node, neighbor)
                print("Neighbor:", neighbor, "Capacity:", edge.get_capacity(), "Flow:", edge.get_flow(), "Cost:", edge.get_cost())
            print("Incoming neighbors:")
            for neighbor in self.inverted_adj_list[node]:
                edge = self.get_edge(neighbor, node)
                print("Neighbor:", neighbor, "Capacity:", edge.get_capacity(), "Flow:", edge.get_flow(), "Cost:", edge.get_cost())
            print("++++++++++++++++++++")


    def get_potential(self, node):
        return self.potential_list[node]
    def set_potential(self, node, potential):
        self.potential_list[node] = potential


    def update_potentials(self, d_source_to_node):
        for node in range(self.num_nodes):
            self.potential_list[node] -= d_source_to_node[node]

    def find_bottleneck_capacity(self, path):
        bottleneck = float('inf')
        for x in range(len(path) - 1):
            i, j = path[x], path[x + 1]
            residual_capacity = self.get_residual_capacity(i, j)
            if residual_capacity < bottleneck:
                bottleneck = residual_capacity
        return bottleneck


    def augment_path(self, path):
        bottleneck = self.find_bottleneck_capacity(path)
        for x in range(len(path) - 1):
            i, j = path[x], path[x + 1]
            curr_flow  = self.get_edge_flow(i, j)
            self.set_edge_flow(i, j, curr_flow + bottleneck)

    def calc_flow(self):
        flow = 0
        drain = 0
        for neighbor in self.get_outgoing_neighbors(0):
            flow += self.get_edge_flow(0, neighbor)
        for neighbor in self.get_incoming_neighbors(6):
            drain += self.get_edge_flow(neighbor, 6)
        is_valid_flow = flow == drain
        return flow, is_valid_flow
