import os
NODES = "nodes"
SOURCE = "source"
SINK = "sink"
ARCS = "arcs"
MAXIMIZE = "Maximize \n"
SUBJECT_TO = "Subject to \n"
BOUNDS = "Bounds \n"
END = "End"
OBJ = "obj: "


class ModelGenerator:
    def __init__(self, filename: str):
        self.nodes = 0
        self.source = 0
        self.sink = 0
        self.arcs = []
        self.filename = filename
        self.objective = MAXIMIZE + OBJ
        self.bounds = BOUNDS
        self.subject_to = SUBJECT_TO
        self.model_name = ""

    def set_model_name(self):
        """Generate the model name by removing the folder path to avoid the path being replaced"""
        filename_without_path = os.path.basename(self.filename)
        filename_folder = os.path.dirname(self.filename)

        self.model_name = filename_without_path.replace("inst", "model").replace("txt", "lp")
        self.model_name = filename_folder + os.path.sep + self.model_name

    def set_up_attributes(self):
        """
        Set up class attributes by reading the file
        """
        with open(self.filename, "r") as flot_instance:
            for line in flot_instance:
                line = line.rstrip().rsplit(" ")

                if len(line) == 2:
                    arg, value = line[0], int(line[1])
                    self.set_up_properties(arg, value)

                elif len(line) == 3:
                    i, j, cost = int(line[0]), int(line[1]), int(line[2])
                    self.add_arc_from_i_to_j(i, j, cost)

    def set_up_properties(self, arg: str, value: int):
        """
        Auxiliary function to setup certain attributes when reading the file
        :param arg: The argument being read (Nodes, source, sink or arcs)
        :param value: The value that has to be set
        :return:
        """
        if arg == NODES:
            self.nodes = value
            self.arcs = [[0 for _ in range(self.nodes)] for _ in range(self.nodes)]
        elif arg == SOURCE:
            self.source = value
        elif arg == SINK:
            self.source = value
        elif arg == ARCS:
            pass  # TODO Don't know what to do with it
        else:
            raise Exception

    def add_arc_from_i_to_j(self, i: int, j: int, cost: int):
        """
        Add outgoing arc cost from node i to j
        :param i: Node i that has outgoing arc
        :param j: Node j that has ingoing arc
        :param cost: Cost of arc i to j
        """
        self.arcs[i][j] = cost

    def write_objective(self):
        """
        Write objective text to be added to model file
        """
        has_outgoing_arcs, outgoing_arcs_string = self.write_line_outgoing_arcs(self.source)
        self.objective += outgoing_arcs_string + "\n"

    def write_line(self, line: int):
        """
        Write line string in the "Subject to" section
        :param line:
        """
        line_string = "l_{}:".format(line)
        has_outgoing_arcs, outgoing_arcs_string = self.write_line_outgoing_arcs(line)
        has_ingoing_arcs, ingoing_arcs_string = self.write_ingoing_arcs(line)
        subject_constraint = " = 0 \n"

        if has_outgoing_arcs and not has_ingoing_arcs:
            subject_constraint = " >= 0 \n"
        elif has_ingoing_arcs and not has_outgoing_arcs:
            subject_constraint = " <= 0 \n"
        elif not has_outgoing_arcs and not has_ingoing_arcs:
            return

        line_string += outgoing_arcs_string + ingoing_arcs_string + subject_constraint
        self.subject_to += line_string

    def write_line_outgoing_arcs(self, line: int):
        """
        Write a lines' outgoing arcs to bounds and return the outgoing arcs line to be written in the constraints, if any
        :param line: the current line that has to be written
        :return: tuple(bool, str) Tuple containing if current line has outgoing arcs and the outgoing arcs constraint string
        """
        outgoing_arcs = self.arcs[line]
        has_outgoing_arcs = False
        outgoing_arcs_string = ""

        for j, arc_cost in enumerate(outgoing_arcs):
            if arc_cost > 0:
                if not has_outgoing_arcs:
                    has_outgoing_arcs = True
                arc_to_string = "x_{}_{}".format(line, j)
                self.bounds += "0 <= " + arc_to_string + " <= {}".format(arc_cost) + "\n"
                outgoing_arcs_string += " + " + arc_to_string
        return has_outgoing_arcs, outgoing_arcs_string

    def write_ingoing_arcs(self, line: int):
        """
        Write a lines' ingoing arcs to bounds and return the ingoing arcs line to be written in the constraints, if any
        :param line: the current line that has to be written
        :return: tuple(bool, str) Tuple containing if current line has ingoing arcs and the ingoing arcs constraint string
        """
        has_ingoing_arcs = False
        ingoing_arcs_string = ""
        ingoing_arc_index = 0

        while ingoing_arc_index < self.nodes:
            ingoing_arc_cost = self.arcs[ingoing_arc_index][line]
            if ingoing_arc_cost > 0:
                if not has_ingoing_arcs:
                    has_ingoing_arcs = True
                ingoing_arcs_string += " - x_{}_{}".format(ingoing_arc_index, line)
            ingoing_arc_index += 1
        return has_ingoing_arcs, ingoing_arcs_string

    def write_model(self):
        """
        Create model file
        """
        self._write_model()

    def _write_model(self):
        """
        Auxiliary function to write_model
        Create model file and write content
        """
        self.set_model_name()
        self.set_up_attributes()
        self.write_objective()

        for line in range(0, self.nodes):
            self.write_line(line)
        with open(self.model_name, "w") as model_out:
            model_out.write(self.objective)
            model_out.write(self.subject_to)
            model_out.write(self.bounds)
            model_out.write(END)


a = ModelGenerator("instances/inst-100-0.2.txt")
a.write_model()
