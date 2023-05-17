from collections import deque

from DirectedFlowGraph import DirectedFlowGraph



def parse_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        num_nodes = int(lines[0].split()[1])
        DFGraph = DirectedFlowGraph(num_nodes)
        for line in lines[4:]:
            try:
                source, target, capacity = map(int, line.split())
                DFGraph.add_edge(source, target, capacity)
            except ValueError:
                #TODO: Remove this once done testing
                try:
                    source, target, capacity, cost = map(int, line.split())
                    DFGraph.add_edge(source, target, capacity, cost)
                except ValueError:
                    print("Error parsing line: " + line)
        return DFGraph




def dijkstra(residual_graph, source, target):
    import heapq
    distances = {node: (float('inf') if node != source else 0) for node in range(residual_graph.num_nodes)}
    unvisited_nodes = [(0,source)] #heapq
    previous_node = {node: None for node in range(residual_graph.num_nodes)}
    while unvisited_nodes:
        current_distance, current_node = heapq.heappop(unvisited_nodes)
        #Skip if curr node has been visited with a shorter distance
        if current_distance > distances[current_node]:
            continue
        #Stop if target reached
        if current_node == target:
            break
        #Explore neighbors of curr node
        for neighbor in residual_graph.get_outgoing_neighbors(current_node):
            edge = residual_graph.get_edge(current_node, neighbor)
            distance = current_distance + edge.get_cost()
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_node[neighbor] = current_node
                heapq.heappush(unvisited_nodes, (distance, neighbor))

    #Reconstruct path /// Using stack is more efficient memory-wise
    path_stack = []
    current_node = target
    while current_node is not None:
        path_stack.append(current_node)
        current_node = previous_node[current_node]
    path = list(reversed(path_stack))
    if path[0] != source:
        return None, None
    return path, distances


def augmenting_paths_method(DFGraph):
    from ResidualFlowGraph import ResidualFlowGraph
    s,t = 0, DFGraph.num_nodes - 1
    path = []
    while True:
        #update residual graph
        res_graph = ResidualFlowGraph(DFGraph)
        if(path == [0, 61, 78, 75, 99]):
            print("here")
        #find augmenting path
        path, d_source_to_node = dijkstra(res_graph, s, t)
        print(path)
        #if no path, then we are done
        if not path:
            break
        #update flow graph
        DFGraph.augment_path(path)
        DFGraph.update_potentials(d_source_to_node)
    return DFGraph.calc_flow()




