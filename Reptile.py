import numpy as np
import math

from Problem import Problem

class Reptile:
    def __init__(self):
        self.problem = Problem()
        self.position = [0] * self.problem.dim

        B_no = np.size(self.problem.UB)
        if B_no == 1:
            for j in range(self.problem.dim):
                self.position[j] = np.random.rand() * (self.problem.UB - self.problem.LB) + self.problem.LB
        else:
            for j in range(self.problem.dim):
                Ub_j = self.problem.UB[j]
                Lb_j = self.problem.LB[j]
                self.position[j] = np.random.randint(0, self.problem.UB[j]) * (Ub_j - Lb_j) + Lb_j

    def move(self, t, T, j, bestj, eta, b, R, N, ES, P, e, X): 
        if(t <= T/4):
            value = bestj - eta * b - R * np.random.rand()
        elif(T / 4 <= t < 2 * T / 4):
            value = bestj * X[np.random.randint(N)].position[j] * ES * np.random.rand()
        elif(2 * T / 4 <= t < 3 * T / 4):
            value = bestj * P * np.random.rand()
        else:
            value = bestj - eta * e - R * np.random.rand()
        self.position[j] = self.discretize(value, j)

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))
    
    def normalize(self, value, min_val, max_val):
        return -6 + (value - min_val) / (max_val - min_val) * (6 - (-6))

    def discretize(self, value, j):
        normalized_value = self.normalize(value, 0, self.problem.UB[j])
        sigmoid_value = self.sigmoid(normalized_value)
        discrete_value = int(np.round(sigmoid_value * self.problem.UB[j]))
        return discrete_value
    
    def isfeasible(self):
        return self.problem.check(self.position)
    def isbetterthan(self, o):
        return self.fitness() > o.fitness()
    def fitness(self):
        return self.problem.scalarization_fit(self.position)
    
    def __str__(self) -> str:
        return f"fit:{self.fitness()} x:{self.position} f:{1 if self.isfeasible() else 0}"
    def copy(self, c):
        self.position = c.position.copy()