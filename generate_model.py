import os
import sys

NODES = "nodes"
SOURCE = "source"
SINK = "sink"
ARCS = "arcs"
MAXIMIZE = "Maximize \n"
SUBJECT_TO = "Subject To \n"
BOUNDS = "Bounds \n"
END = "End\n"
OBJ = "obj: "


class GLPK_Solver:
    def __init__(self, filename: str):
        self.nodes = 0
        self.source = 0
        self.sink = 0
        self.arcs = 0
        self.filename = filename
        self.objective = ""
        self.bounds = []
        self.subject_to = [[]]
        self.model_name = ""
        self.already_added_lines = set()

    def set_model_name(self):
        """Generate the model name"""
        filename = os.path.basename(self.filename)
        modelFilename =  filename.replace("inst", "model").replace(".txt", "")
        dir_path = os.path.dirname(self.filename)
        self.model_name =  os.path.join(dir_path, modelFilename)

    def set_up_attributes(self):
        """
        Set up class values and add arcs string
        """
        with open(self.filename, "r") as flot_instance:
            for line in flot_instance:
                arguments = line.split()
                if len(arguments) == 2:
                    self.set_up_properties(*arguments)
                elif arguments:
                    if tuple(arguments[:2]) not in self.already_added_lines:
                        self.already_added_lines.add(tuple(arguments[:2]))
                        self.add_arc(*arguments)

    def set_up_properties(self, arg: str, value: str):
        """
        Auxiliary function to set up certain attributes when reading the file
        :param arg: The argument being read (Nodes, source, sink or arcs)
        :param value: The value that has to be set
        :return:
        """
        if arg == NODES:
            self.nodes = int(value)
            self.subject_to = [f"x_{node}: " for node in range(self.nodes)]
        elif arg == SOURCE:
            self.source = value
        elif arg == SINK:
            self.sink = value
        elif arg == ARCS:
            self.arcs = int(value)
        else:
            raise Exception

    def add_arc(self, source: str, destination: str, flow: str):
        """
        Add an arc from the source node to the destination node
        Build the bound constraint with the flow as upper bound
        """
        if source != destination:
            self.bounds.append(f"0 <= x_{source}_{destination} <= {flow}")
            self.subject_to[int(source)] += f" + x_{source}_{destination}"
            self.subject_to[int(destination)] += f" - x_{source}_{destination}"

    def build_constraints(self):
        """
        Build problem constraints
        """
        for node in map(str, range(self.nodes)):
            if node == self.source:
                self.objective = "".join(self.subject_to[int(node)][4:]) + "\n"
            self.subject_to[int(node)] += f" {'>=' if node == self.source else '<=' if node == self.sink else '='} 0"

    def write_to_file(self):
        """
        Write objective, constraints and bounds to file
        """
        self.subject_to = "\n".join(self.subject_to) + "\n"
        self.bounds = "\n".join(self.bounds) + "\n"
        model_content = f"{MAXIMIZE + OBJ}{self.objective}{SUBJECT_TO}{self.subject_to}{BOUNDS}{self.bounds}{END}"
        with open(self.model_name + ".lp", "w") as model_out:
            model_out.write(model_content)

    def generate_model(self):
        self.set_model_name()
        self.set_up_attributes()
        self.build_constraints()
        self.write_to_file()

    def solve_model(self):
        """
        Solve model using glpsol --lp
        """
        self.generate_model()
        os.system(f"glpsol --lp {self.model_name}.lp -o {self.model_name}.sol")


class GLPK_Graph:
    def __init__(self, nodes, source, sink, filename):
        self.flow_graph = [[0 for i in range(nodes)] for _ in range(nodes)]
        self.max_capacity_graph = [[0 for i in range(nodes)] for _ in range(nodes)]
        self.source = int(source)
        self.sink = int(sink)
        self.filename = filename
        self.visited = []

    def get_graph_info(self):
        with open(f"{self.filename}{'.sol'}", 'r') as file:
            lines = file.readlines()
            count = 0
            for line in lines:
                columns = line.split()
                if count == 2:
                    try:
                        if columns and columns[2] != "--":
                            _, source, destination = columns[1].split("_")
                            flow = int(columns[3])
                            capacity = int(columns[5])
                            source, destination = int(source), int(destination)
                            self.flow_graph[source][destination] = flow
                            self.max_capacity_graph[source][destination] = capacity
                    except ValueError:
                        break
                if columns and columns[0] == "No.":

                    count += 1

    def find_s_t_cut(self):
        self.get_graph_info()
        self._find_s_t_cut()

    def _find_s_t_cut(self):
        queue = [self.source]
        self.visited = []
        while len(queue) > 0:
            node = queue.pop()
            self.visited.append(node)
            for destination, destination_flow in enumerate(self.flow_graph[node]):
                if destination_flow and destination_flow < self.max_capacity_graph[node][destination] and destination not in self.visited:
                    queue.append(destination)

    def is_optimal(self):
        self.find_s_t_cut()
        return self.sink not in self.visited


def main(filename: str):
    generator = GLPK_Solver(filename)
    generator.solve_model()
    print(f"Found solution for {generator.model_name}")
    graph = GLPK_Graph(generator.nodes, generator.source, generator.sink, generator.model_name)
    print("GLPK Solution is optimal: ", graph.is_optimal())

if __name__ == "__main__":
    try:
        instance_to_solve = sys.argv[1]
        main(instance_to_solve)
    except IndexError:
        print("Enter a filename")
    except FileNotFoundError:
        print("Enter a correct filename")



