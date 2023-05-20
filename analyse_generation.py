import time
import matplotlib.pyplot as plt
import numpy as np
from generate_model import *


count = 0
instances = [_ for _ in range(1, 11 )]
solveDensity1 = []
solveDensity2 = []
solveDensity3 = []

for i in range(1, 15):
    with open(f"results{i}.txt", "r") as file:
        solveDensity1tmp = []
        solveDensity2tmp = []
        solveDensity3tmp = []
        for line in file:
            instance, generate_time, solve_time= line.strip().split(",")
            timesToGenerate.append(float(generate_time))
            timesToSolve.append(float(solve_time))
            #arcs.append(int(arc))d
            if count == 0:
                solveDensity1tmp.append(float(solve_time))
            elif count == 1:
                solveDensity2tmp.append(float(solve_time))
            else:
                solveDensity3tmp.append(float(solve_time))
            count += 1
            if count % 3 == 0:
                count = 0
    solveDensity1.append(solveDensity1tmp)
    solveDensity2.append(solveDensity2tmp)
    solveDensity3.append(solveDensity3tmp)
solveDensity1 = np.array(solveDensity1)
solveDensity2 = np.array(solveDensity2)
solveDensity3 = np.array(solveDensity3)
#plt.plot(instances, timesToGenerate, marker='o', linestyle='-',label="Time to generate instance")
#plt.plot(instances, timesToSolve, marker='o', linestyle='-', label="Time to solve instance")
#plt.xlabel("Instance number")
#plt.ylabel("Time")
mean_values = np.mean(solveDensity1, axis=0)
std_values = np.std(solveDensity1, axis=0)

mean_values1 = np.mean(solveDensity2, axis=0)
std_values1 = np.std(solveDensity2, axis=0)

mean_values2 = np.mean(solveDensity3, axis=0)
std_values2 = np.std(solveDensity3, axis=0)
t = np.arange(0, 15, 1)
# Plot the mean line
plt.plot(mean_values, color='green', label='Mean for instances of density 1')
# Plot the shaded area representing the standard deviation
plt.fill_between(t, mean_values - std_values, mean_values + std_values, color='red',
                    alpha=0.3, label='Standard Deviation for instances of density 1')
plt.plot(mean_values1, color='red', label='Mean for instances of density 2')
# Plot the shaded area representing the standard deviation
plt.fill_between(t, mean_values1 - std_values1, mean_values1 + std_values1, color='blue',
                    alpha=0.3, label='Standard Deviation for instances of density 2')
plt.plot(mean_values2, color='blue', label='Mean for instances of density 3')
# Plot the shaded area representing the standard deviation
plt.fill_between(t, mean_values2 - std_values2, mean_values2 + std_values2, color='green',
                    alpha=0.3, label='Standard Deviation for instances of density 3')

# Set labels and title
plt.xlabel('Number of instance')
plt.ylabel('Time to solve')
plt.title('Mean time to solve instance with standard deviation')

# Display the legend
plt.legend()


plt.show()
