import numpy as np
from app.src.constants import *
from abc import ABC, abstractmethod
from scipy.integrate import solve_ivp
from matplotlib import pyplot as plt


class Simulation(ABC):

    def __init__(self, local_v1_0, local_v2_0, local_i3_0, times):
        self.initial_values = np.array([local_v1_0, local_v2_0, local_i3_0])
        self.times = times
        self.solution = solve_ivp(self.dx, (0, end), self.initial_values, t_eval=self.times, dense_output=True)

    @abstractmethod
    def vr(self, _, __, ___):
        pass

    @abstractmethod
    def e(self, _, __):
        pass

    def dx(self, t, x):
        v1, v2, i3 = x
        return np.array(
            [
                a * (v2 - v1) + chuas_characteristic(self.vr(t, v1, v2)),
                b * (v1 - v2) + c * i3,
                d * v2
            ]
        )


    def print_simulation_result(self, name):
        plt.title("Simulation " + name)
        plt.plot(self.times, self.solution.y[0], label="v1")
        plt.plot(self.times, 100 * self.solution.y[1], label="v2")
        plt.plot(self.times, 1000 * self.solution.y[2], label="i3")
        plt.axis([0, end, -5, 5])
        plt.legend(["v1 (V)", "v2 (10mV)", "i3 (mA)"])
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


def chuas_characteristic(v):
    return e * v + f * (abs(v + E) - abs(v - E))


def get_k_from_t(t):
    if t >= end:
        return number - 1
    return int(t * number / end)

def get_t_from_k(k):
    return k*end/number
