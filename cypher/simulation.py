import numpy as np
from constants import *
from abc import ABC, abstractmethod
from scipy.integrate import solve_ivp
from matplotlib import pyplot as plt


class Simulation(ABC):

    def __init__(self, local_v1_0, local_v2_0, local_i3_0, times):
        self.initial_values = np.array([local_v1_0, local_v2_0, local_i3_0])
        self.times = times
        self.i = 0

    @abstractmethod
    def vr(self, _, __, ___):
        pass

    @abstractmethod
    def e(self, _, __):
        pass

    def dx(self, t, x):
        if self.i%100 == 0:
            print(t, x)
        self.i+=1
        v1, v2, i3 = x
        vr = self.vr(t, v1, v2)
        return np.array(
            [
                dv1(v1, v2, vr),
                dv2(v1, v2, i3),
                di3(v2)
            ]
        )

    def solve(self):
        x = solve_ivp(self.dx, (0, end), self.initial_values, t_eval=self.times, method='RK23',
                      rtol=1e-2, atol=1e-3)
        print("hey")
        return x[:, 0], x[:, 1], x[:, 2]

    def print_simulation_result(self, solution, name):
        plt.title("Simulation " + name)
        plt.plot(self.times, solution[0], label="v1")
        plt.plot(self.times, 10 * solution[1], label="v2")
        plt.plot(self.times, 1000 * solution[2], label="i3")
        plt.axis([0, end, -5, 5])
        plt.legend(["v1 (V)", "v2 (0.1V)", "i3 (mA)"])
        plt.show()


def f1(x, k):
    sum = x + k
    while sum <= -h:
        sum += 2 * h
    while sum >= h:
        sum -= 2 * h
    return sum


def _f1(x, k):
    sum = x+k
    if -2 * h <= sum <= -h:
        return sum + 2 * h
    if -h < sum < h:
        return sum
    if h <= sum <= 2 * h:
        return sum - 2 * h
    raise ValueError("Invalid value", x, k, get_t_from_k(k), sum, 2*h)


def dv1(v1, v2, vr):
    return (G * (v2 - v1) - f(vr)) / C1


def dv2(v1, v2, i3):
    return (G * (v1 - v2)+i3) / C2


def di3(v2):
    return -v2 / L


def f(v):
    return Gb * v + 0.5 * (Ga - Gb) * (abs(v + E) - abs(v - E))


def get_k_from_t(t):
    if t >= end:
        return number - 1
    return int(t * number / end)

def get_t_from_k(k):
    return k*end/number
