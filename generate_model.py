import os
from collections import defaultdict

NODES = "nodes"
SOURCE = "source"
SINK = "sink"
ARCS = "arcs"
MAXIMIZE = "maximize \n"
SUBJECT_TO = "subject to \n"
BOUNDS = "bounds \n"
END = "end"
OBJ = "obj: "


class ModelGenerator:
    def __init__(self, filename: str):
        self.nodes = 0
        self.source = 0
        self.sink = 0
        self.filename = filename
        self.objective = MAXIMIZE + OBJ
        self.bounds = [BOUNDS]
        self.subjectTo = [SUBJECT_TO]
        self.modelName = ""

        self.ingoingArcs = defaultdict(set)
        self.outgoingArcs = defaultdict(set)

    def setModelName(self):
        """Generate the model name by removing the folder path to avoid the path being replaced"""
        filenameWithoutPath = os.path.basename(self.filename)
        filenameFolder = os.path.dirname(self.filename)

        self.modelName = filenameWithoutPath.replace("inst", "model").replace("txt", "lp")
        self.modelName = filenameFolder + os.path.sep + "solutions" + os.path.sep + self.modelName

    def setUpAttributes(self):
        """
        Set up class attributes by reading the file
        """
        with open(self.filename, "r") as flot_instance:
            lines = flot_instance.read().split("\n")
            for line in lines:
                arguments = line.split()
                if len(arguments) == 2:
                    self.setUpProperties(*arguments)
                elif arguments:
                    arc = [int(element) for element in arguments]
                    self.addArc(*arc)

    def setUpProperties(self, arg: str, value: str):
        """
        Auxiliary function to set up certain attributes when reading the file
        :param arg: The argument being read (Nodes, source, sink or arcs)
        :param value: The value that has to be set
        :return:
        """
        value = int(value)
        if arg == NODES:
            self.nodes = value
        elif arg == SOURCE:
            self.source = value
        elif arg == SINK:
            self.sink = value
        elif arg == ARCS:
            pass  # TODO Don't know what to do with it
        else:
            raise Exception

    def addArc(self, source, destination, flow):
        if source != destination and source != self.sink and destination != self.source:
            self.ingoingArcs[destination].add(source)
            self.outgoingArcs[source].add(destination)
            self.bounds.append(f"0 <= x_{source}_{destination} <= {flow}")

    def buildConstraints(self):
        for node in range(self.nodes):
            arcConstraint = f"x_{node}: "
            for destination in self.outgoingArcs[node]:
                arcConstraint += f" - x_{node}_{destination}"
            for source in self.ingoingArcs[node]:
                arcConstraint += f" + x_{source}_{node}"
            if node == self.source:
                arcConstraint += " >= 0"
                self.objective += arcConstraint + "\n"
            elif node == self.sink:
                arcConstraint += " <= 0"
            else:
                arcConstraint += " = 0"
            self.subjectTo.append(arcConstraint)

    def writeToFile(self):
        self.subjectTo = "\n".join(self.subjectTo) + "\n"
        self.bounds = "\n".join(self.bounds) + "\n"
        modelContent = f"{self.objective}{self.subjectTo}{self.bounds}{END}"
        with open(self.modelName, "w") as modelOut:
            modelOut.write(modelContent)

    def generateModel(self):
        self.setModelName()
        self.setUpAttributes()
        self.buildConstraints()
        self.writeToFile()

def main():
    generate_model = "Instances/inst-1500-0.3.txt"
    generator = ModelGenerator(generate_model)
    generator.generateModel()

if __name__ == "__main__":
    main()
