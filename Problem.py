import numpy as np

class Problem:
    def __init__(self):
        self.dim = 5
        self.LB = [0, 0, 0, 0, 0]
        self.UB = [15, 10, 25, 4, 30]

    def check(self, solution):
        x1, x2, x3, x4, x5 = solution
        limit_x = [ x1 <= 15, x2 <= 10, x3 <= 25, x4 <= 4, x5 <= 30 ]
        budget_constraints = [
            194 * x1 + 320 * x2 <= 3800,
            68 * x3 + 113 * x4 <= 2800,
            68 * x3 + 17 * x5 <= 3500,
            #np.dot([194, 320, 68, 113, 17], solution) <= 4000 # e-constraint
        ]
        if all(limit_x) and all(budget_constraints): return True
        else: return False

    def scalarization_fit(self, solution):
        min_hat, max_hat, c_hat = 6338, 3890, 150000

        mn = np.dot([194, 320, 68, 113, 17], solution) # Minimización
        mx = np.dot([83, 92, 54, 73, 27], solution) # Maximización

        value = ((mx/ max_hat) * 0.1) + (((c_hat - mn)/ (c_hat - min_hat)) * 0.9)
        return value

    def fit(self, solution): # e-constraint
        return np.dot([83, 92, 54, 73, 27], solution) # Maximizar