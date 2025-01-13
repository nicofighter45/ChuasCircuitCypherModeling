import numpy as np
from constants import *
from abc import ABC, abstractmethod
from scipy.integrate import solve_ivp
from matplotlib import pyplot as plt


def vrf(t, v1, v2):
    tot = f1(0.2 * np.sin(t), v2)
    for _ in range(n - 1):
        tot = f1(tot, v2)
    return v1 - tot

class Simulation2:

    def __init__(self, local_v1_0, local_v2_0, local_i3_0, times):
        self.initial_values = np.array([local_v1_0, local_v2_0, local_i3_0])
        self.times = times

    def dx(self, t, x):
        v1, v2, i3 = x
        vr = vrf(t, v1, v2)
        return np.array(
            [
                a*(v2-v1) + e*vr + f*(abs(vr+E)-abs(vr-E)),
                b*(v1-v2) + c*i3,
                d*v2
            ]
        )

    def solve(self):
        x = solve_ivp(self.dx, (0, end), self.initial_values, t_eval=self.times)
        return x.y[0], x.y[1], x.y[2]

    def print_simulation_result(self, solution, name):
        plt.title("Simulation " + name)
        plt.plot(self.times[9000:], self.vr_list(solution)[1000:], label="i3")
        plt.legend(["vr"])

        plt.show()

    def vr_list(self, solved_simulation):
        vr_list = []
        for t in self.times:
            k = get_k_from_t(t)
            vr_list.append(vrf(t, solved_simulation[0][k], solved_simulation[1][k]))
        return np.array(vr_list)


def f1(x, k):
    sum = x + k
    while sum <= -h:
        sum += 2 * h
    while sum >= h:
        sum -= 2 * h
    return sum


def get_k_from_t(t):
    if t >= end:
        return number - 1
    return int(t * number / end)

def get_t_from_k(k):
    return k*end/number


sim = Simulation2(v1_0, v2_0, i3_0, np.array([i * end / number for i in range(number)]))
simu = sim.solve()
sim.print_simulation_result(simu, "encryption")
