import numpy as np
from constants import *
from abc import ABC, abstractmethod
from scipy.integrate import odeint
from matplotlib import pyplot as plt


class Simulation(ABC):

    def __init__(self, local_v1_0, local_v2_0, local_i3_0):
        self.initial_values = np.array([local_v1_0, local_v2_0, local_i3_0])
        self.times = np.array([i * end / number for i in range(number)])
        self.t = 0
        self.v1, self.v2, self.i3 = local_v1_0, local_v2_0, local_i3_0

    @abstractmethod
    def vr(self):
        pass

    @abstractmethod
    def e(self):
        pass

    def dv1(self):
        return (G * (self.v2 - self.v1) - f(self.vr())) / C1

    def dv2(self):
        return (G * (self.v1 - self.v2) + self.i3) / C2

    def di3(self):
        return -self.v2 / L

    def dx(self, x, local_t):
        self.v1, self.v2, self.i3 = x
        self.t = local_t
        return np.array(
            [
                self.dv1(),
                self.dv2(),
                self.di3()
            ]
        )

    def solve(self):
        x = odeint(self.dx, self.initial_values, self.times)
        v1_list = x[:, 0]
        v2_list = x[:, 1]
        i3_list = x[:, 2]
        return v1_list, v2_list, i3_list

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
    while sum < -h:
        sum += 2 * h
    while sum > h:
        sum -= 2 * h
    return sum


@DeprecationWarning
def old_f1(x, k):
    sum = x+k
    if -2 * h <= sum <= -h:
        return sum + 2 * h
    if -h < sum < h:
        return sum
    if h <= sum <= 2 * h:
        return sum - 2 * h
    raise ValueError("Invalid value", x, k, sum, 2*h)


def f(v):
    return Gb * v + 0.5 * (Ga - Gb) * (abs(v + E) - abs(v - E))


def get_k_from_t(t):
    if t >= end:
        return number - 1
    return int(t * number / end)
