import numpy as np
import math


class Solution:
    def __init__(self, x_0, y_0, x_f, n):
        self.x_0 = x_0
        self.y_0 = y_0
        self.x_f = x_f
        self.n = n
        self.h = float((x_f - x_0) / n)
        self.X = np.linspace(x_0, x_f, self.n+1)
        self.Y = np.zeros(self.n+1)
        self.Y[0] = y_0

    def solve(self):
        pass

    def error(self, y):
        e = []
        if len(y) == len(self.Y):
            e = abs(y - self.Y)
        return e

    @staticmethod
    def maxError(e):
        return max(e)

    @staticmethod
    def func(x, y):
        return (2 - y ** 2) / (2 * y * x ** 2)


class ExactSolution(Solution):
    def __init__(self, x_0, y_0, x_f, n):
        super().__init__(x_0, y_0, x_f, n)
        self.c = (y_0**2 - 2)/ math.exp(1/x_0)

    def solve(self):
        for i in range(1, self.n+1):
            self.Y[i] = math.sqrt(2 + self.c * math.exp(1 / self.X[i]))
        return self.X, self.Y


class EulerMethod(Solution):
    def __init__(self, x_0, y_0, x_f, n):
        super().__init__(x_0, y_0, x_f, n)

    def solve(self):
        for i in range(0, self.n):
            self.Y[i + 1] = self.Y[i] + self.h * self.func(self.X[i], self.Y[i])
        return self.X, self.Y


class ImprovedEulerMethod(Solution):
    def __init__(self, x_0, y_0, x_f, n):
        super().__init__(x_0, y_0, x_f, n)
        self.k1 = np.zeros(self.n+1)
        self.k2 = np.zeros(self.n+1)

    def solve(self):
        for i in range(0, self.n+1):
            self.k1[i] = self.func(self.X[i], self.Y[i])
            self.k2[i] = self.func(self.X[i] + self.h, self.Y[i] + self.h * self.k1[i])
            if i < self.n:
                self.Y[i + 1] = self.Y[i] + self.h / 2 * (self.k1[i] + self.k2[i])
        return self.X, self.Y


class RungeKuttaMethod(Solution):
    def __init__(self, x_0, y_0, x_f, n):
        super().__init__(x_0, y_0, x_f, n)
        self.k1 = np.zeros(self.n+1)
        self.k2 = np.zeros(self.n+1)
        self.k3 = np.zeros(self.n+1)
        self.k4 = np.zeros(self.n+1)

    def solve(self):
        for i in range(0, self.n+1):
            self.k1[i] = self.func(self.X[i], self.Y[i])
            self.k2[i] = self.func(self.X[i] + self.h / 2, self.Y[i] + self.h / 2 * self.k1[i])
            self.k3[i] = self.func(self.X[i] + self.h / 2, self.Y[i] + self.h / 2 * self.k2[i])
            self.k4[i] = self.func(self.X[i] + self.h, self.Y[i] + self.h * self.k3[i])
            if i < self.n:
                self.Y[i + 1] = self.Y[i] + self.h / 6 * (self.k1[i] + 2 * self.k2[i] + 2 * self.k3[i] + self.k4[i])
        return self.X, self.Y


class TotalError:
    def __init__(self, n_0, n_f):
        self.n_0 = n_0
        self.n_f = n_f
        self.X = np.linspace(self.n_0, self.n_f, self.n_f - self.n_0 + 1)
        self.Y = np.zeros(self.n_f - self.n_0 + 1)

    def calculate(self, x_0, y_0, x_f):
        n_0 = self.n_0
        n_f = self.n_f
        em_te_y = np.zeros(n_f-n_0+1)
        iem_te_y = np.zeros(n_f-n_0+1)
        rkm_te_y = np.zeros(n_f-n_0+1)
        for i in range(n_f-n_0+1):
            ex = ExactSolution(x_0, y_0, x_f, n_0+i)
            ex.solve()
            em = EulerMethod(x_0, y_0, x_f, n_0+i)
            em.solve()
            iem = ImprovedEulerMethod(x_0, y_0, x_f, n_0+i)
            iem.solve()
            rkm = RungeKuttaMethod(x_0, y_0, x_f, n_0+i)
            rkm.solve()
            em_te_y[i] = em.maxError(em.error(ex.Y))
            iem_te_y[i] = iem.maxError(iem.error(ex.Y))
            rkm_te_y[i] = rkm.maxError(rkm.error(ex.Y))
        return em_te_y, iem_te_y, rkm_te_y
