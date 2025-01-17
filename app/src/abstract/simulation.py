import numpy as np
from app.src.constants import *
from abc import ABC, abstractmethod
from scipy.integrate import solve_ivp
from matplotlib import pyplot as plt


class Simulation(ABC):
    """Abstract class for simulation, contains the simulation of the Chua's circuit without the implementation of vr and e"""

    def __init__(self, local_v1_0, local_v2_0, local_i3_0, times):
        self.__initial_values = np.array([local_v1_0, local_v2_0, local_i3_0])
        self._times = times
        # solve the system of differential equations with scipy
        self.solution = solve_ivp(self.__dx, (0, end), self.__initial_values, t_eval=self._times, dense_output=True)

    @abstractmethod
    def vr(self, _, __, ___):
        pass

    @abstractmethod
    def e(self, _, __):
        pass

    def __dx(self, t, x):
        v1, v2, i3 = x
        return np.array(
            [
                a * (v2 - v1) + chuas_characteristic(self.vr(t, v1, v2)),
                b * (v1 - v2) + c * i3,
                d * v2
            ]
        )

    def print_simulation_result(self, name, i, j):
        fig, axs = plt.subplots()
        fig.patch.set_facecolor((BACKGROUND_COLOR[0] / 255, BACKGROUND_COLOR[1] / 255, BACKGROUND_COLOR[2] / 255))
        axs.set_title("Electrical " + name + " for the " + str(j + 1) + "th character")
        axs.set_xlabel('Time (ms)')
        ts = [1000 * t for t in self._times]
        axs.plot(ts, self.solution.y[0], label="v1")
        axs.plot(ts, 100 * self.solution.y[1], label="v2")
        axs.plot(ts, 1000 * self.solution.y[2], label="i3")
        axs.legend(["v1 (V)", "v2 (10mV)", "i3 (mA)"])
        fig.savefig(f'app/ressources/export/graph{i}{j}.png')


def f1(x, k):
    sum = x + k
    while sum <= -h:
        sum += 2 * h
    while sum >= h:
        sum -= 2 * h
    return sum


def chuas_characteristic(v):
    return e * v + f * (abs(v + E) - abs(v - E))


def get_k_from_t(t):
    if t >= end:
        return number - 1
    return int(t * number / end)

def get_t_from_k(k):
    return k*end/number
