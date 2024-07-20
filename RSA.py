import numpy as np
import random as rnd

from Problem import Problem
from Reptile import Reptile

class RSA:
    def __init__(self, T, N):
        self.T = T
        self.N = N

        self.a = 0.1
        self.b = 0.1
        self.epsilon = np.finfo(float).eps
        self.X = []
        self.c = Reptile()

        self.Eta = 0
        self.P = 0
        self.R = 0
        self.ES = 0

        self.Prob = Problem()
        self.conv = np.zeros(T)
        self.sol = []
        self.lastIter = 0

    def getEta(self, j): 
        return self.c.position[j] * self.P

    def getP(self, i, j):
        B_no = np.size(self.Prob.UB)
        if B_no == 1:
            return self.a + ( self.X[i].position[j] - np.mean(self.X[i].position) ) / (self.c.position[j] * (self.Prob.UB - self.Prob.LB) + self.epsilon)
        else:
            return self.a + ( self.X[i].position[j] - np.mean(self.X[i].position) ) / (self.c.position[j] * (self.Prob.UB[j] - self.Prob.LB[j]) + self.epsilon)

    def getR(self, j):
        return self.c.position[j] - self.X[rnd.randint(0, self.N-1)].position[j] / (self.c.position[j] + self.epsilon)
    
    def getES(self, t, T):
        #return 2 *  rnd.choice([-1, 1]) * (1 - (1 / T))
        return 2 *  np.random.randint(-1, 2) * (1 - (t / T))

    def solve(self):
        self.init()
        self.evolve()
        return self.conv, self.sol, self.lastIter

    def init(self):
        self.X = list()
        for _ in range(self.N):
            while True:
                c = Reptile()
                if c.isfeasible():
                    break
            self.X.append(c)

    def evolve(self):
        self.c.copy(self.X[0]) 
        for i in range(self.N):
            if self.X[i].isbetterthan(self.c): 
                self.bestF = self.X[i].fitness() 
                self.c.copy(self.X[i])

        t = 1
        while t < self.T + 1: 
            self.ES = self.getES(t, self.T)
            for i in range(self.N): 
                aux = Reptile()
                while True:
                    aux.copy(self.X[i])
                    #print(f'aux copy: {aux}')
                    for j in range(self.Prob.dim):
                        self.R = self.getR(j)
                        self.P = self.getP(i,j)
                        self.Eta = self.getEta(j)
                        aux.move(t, self.T, j, self.c.position[j], self.Eta, self.b, self.R, self.N, self.ES, self.P, self.epsilon, self.X)                    
                    
                    if aux.isfeasible():
                        self.X[i].copy(aux)
                        break

                if self.X[i].isbetterthan(self.c):
                    self.lastIter = t
                    self.c.copy(self.X[i])
            
            self.conv[t - 1] = self.c.fitness()
            self.sol.append(self.c.position)
            t += 1
        print(self.c)