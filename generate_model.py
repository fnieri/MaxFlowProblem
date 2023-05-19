import os
import sys
from collections import defaultdict
import time
import matplotlib.pyplot as plt
NODES = "nodes"
SOURCE = "source"
SINK = "sink"
ARCS = "arcs"
MAXIMIZE = "Maximize \n"
SUBJECT_TO = "Subject To \n"
BOUNDS = "Bounds \n"
END = "End\n"
OBJ = "obj: "

timesToGenerate = []
timesToSolve = []
instances = []
arcs = []


class ModelGenerator:
    def __init__(self, filename: str):
        self.nodes = 0
        self.source = 0
        self.sink = 0
        self.arcs = 0
        self.filename = filename
        self.objective = ""
        self.bounds = []
        self.subjectTo = [[]]
        self.modelName = ""
        self.alreadyAddedLines = set()

    def setModelName(self):
        """Generate the model name"""
        self.modelName = self.filename.replace("inst", "model").replace(".txt", "")

    def setUpAttributes(self):
        """
        Set up class values and add arcs string
        """
        with open(self.filename, "r") as flot_instance:
            for line in flot_instance:
                arguments = line.split()
                if len(arguments) == 2:
                    self.setUpProperties(*arguments)
                elif arguments:
                    if tuple(arguments[:2]) not in self.alreadyAddedLines:
                        self.alreadyAddedLines.add((arguments[0], arguments[1]))
                        self.addArc(*arguments)

    def setUpProperties(self, arg: str, value: str):
        """
        Auxiliary function to set up certain attributes when reading the file
        :param arg: The argument being read (Nodes, source, sink or arcs)
        :param value: The value that has to be set
        :return:
        """
        if arg == NODES:
            self.nodes = int(value)
            self.subjectTo = [f"x_{node}: " for node in range(self.nodes)]
        elif arg == SOURCE:
            self.source = value
        elif arg == SINK:
            self.sink = value
        elif arg == ARCS:
            self.arcs = int(value)
        else:
            raise Exception

    def addArc(self, source: str, destination: str, flow: str):
        """
        Add an arc from the source to the 2
        """
        if source != destination and source != self.sink and destination != self.source:
            self.bounds.append(f"0 <= x_{source}_{destination} <= {flow}")
            self.subjectTo[int(source)] += f" + x_{source}_{destination}"
            self.subjectTo[int(destination)] += f" - x_{source}_{destination}"

    def buildConstraints(self):
        """
        Build problem constraints
        """
        #Add flow formulation
        for node in map(str, range(self.nodes)):
            #Add objective
            if node == self.source:
                self.objective = "".join(self.subjectTo[int(node)][4:]) + "\n"
            self.subjectTo[int(node)] += f" {'>=' if node == self.source else '<=' if node == self.sink else '='} 0"

    def writeToFile(self):
        """
        Write objective, constraints and bounds to file
        :return:
        """
        self.subjectTo = "\n".join(self.subjectTo) + "\n"
        self.bounds = "\n".join(self.bounds) + "\n"
        modelContent = f"{MAXIMIZE + OBJ}{self.objective}{SUBJECT_TO}{self.subjectTo}{BOUNDS}{self.bounds}{END}"
        with open(self.modelName + ".lp", "w") as modelOut:
            modelOut.write(modelContent)

    def generateModel(self):
        startTime = time.time()
        self.setModelName()
        self.setUpAttributes()
        self.buildConstraints()
        self.writeToFile()
        endTime = time.time()
        timesToGenerate.append(endTime - startTime)

    def solveModel(self):
        self.generateModel()
        startTime = time.time()
        os.system(f"glpsol --lp {self.modelName}.lp -o {self.modelName}.sol")
        endTime = time.time()
        timesToSolve.append(endTime - startTime)


class Graph:
    def __init__(self, nodes, source, sink, filename):
        self.flowGraph = [[0 for i in range(nodes)] for _ in range(nodes)]
        self.maxCapacityGraph = [[0 for i in range(nodes)] for _ in range(nodes)]
        self.source = int(source)
        self.sink = int(sink)
        self.filename = filename
        self.visited = []

    def getGraphInfo(self):
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
                            self.flowGraph[source][destination] = flow
                            self.maxCapacityGraph[source][destination] = capacity

                    except ValueError:
                        break
                if columns and columns[0] == "No.":
                    count += 1

    def findSTCut(self):
        self.getGraphInfo()
        self._findSTCut()

    def _findSTCut(self):
        queue = [self.source]
        self.visited = []
        while len(queue) > 0:
            node = queue.pop()
            self.visited.append(node)
            for destination, destinationFlow in enumerate(self.flowGraph[node]):
                if destinationFlow and destinationFlow < self.maxCapacityGraph[node][destination] and destination not in self.visited:
                    queue.append(destination)

    def isOptimal(self):
        self.findSTCut()
        return self.sink not in self.visited

def main():
    instance = 0
    for nodes in range(100, 1600, 100):
        for density in range(1, 4):
            generate_model = f"Instances/inst-{nodes}-0.{density}.txt"
            generator = ModelGenerator(generate_model)
            generator.solveModel()
            graph = Graph(generator.nodes, generator.source, generator.sink, generator.modelName)
            print(graph.isOptimal())
            
#def main(filename: str):
 #   model_gen = ModelGenerator(filename)
  #  model_gen.solveModel()
   # graph = Graph(model_gen.nodes, model_gen.source, model_gen.sink, model_gen.modelName)
    #print(graph.isOptimal())

if __name__ == "__main__":
    try:
        filename = sys.argv[1]
        #main(filename)
        main()
    except IndexError:
        print("Enter a filename")
    """
    with open("results.txt", "r") as file:
        for line in file:
            instance, generate_time, solve_time, arc = line.strip().split(",")
            instances.append(int(instance))
            timesToGenerate.append(float(generate_time))
            timesToSolve.append(float(solve_time))
            arcs.append(int(arc))

    plt.plot(instances, timesToGenerate, marker='o', linestyle='-',label="Time to generate instance")
    plt.plot(instances, timesToSolve, marker='o', linestyle='-', label="Time to solve instance")
    plt.xlabel("Instance number")
    plt.ylabel("Time")
    # Adjust the x-axis tick spacing
    plt.xticks(instances[::10])  # Set the x-axis ticks at every 10th instance
    plt.xticks(rotation=45, ha='right')  # Rotate the x-axis labels by 45 degrees and align them to the right
    plt.scatter(instances, timesToGenerate, color='red')
    plt.scatter(instances, timesToSolve, color='blue')

    plt.legend()
    plt.show()

    for j in range(len(arcs)-1):
        for i in range(len(arcs)-1):
            if arcs[i] > arcs[i+1]:
                arcs[i], arcs[i+1] = arcs[i+1], arcs[i]
                timesToSolve[i], timesToSolve[i+1] = timesToSolve[i+1], timesToSolve[i]
                timesToGenerate[i], timesToGenerate[i+1] = timesToGenerate[i+1], timesToGenerate[i]
    plt.plot(arcs, timesToSolve)
    plt.xlabel("Number of arcs")
    plt.ylabel("Time to solve")
    plt.show()
    """


