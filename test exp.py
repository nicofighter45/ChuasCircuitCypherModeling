from math import *
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as spi
import test

# electrical constants
C2, C1, L, G, Ga, Gb, E = 50e-9, 5.56e-9, 7.14e-3, 0.7e-3, -0.8e-3, -0.5e-3, 1

# simulation constants
n = 30
h = 0.4

def f(v):
    return Gb*v + 0.5*(Ga-Gb)*(abs(v+E) - abs(v-E))

def dv1(v1, v2, vr):
    return (G*(v2-v1) -f(vr))/C1

def dv2(v1, v2, i3):
    return (G*(v1-v2) + i3)/C2

def di3(v2):
    return -v2/L

def f1(x, k):
    if -2*h <= x + k <= -h:
        return x+k+2*h
    if -h < x + k < h:
        return x+k
    if h <= x + k <= 2*h:
        return x+k-2*h
    print(x+k)
    raise Exception("Invalid value")

def y(v1, vr):
    return v1 - vr

def p(y, v2):
    tot = f1(y, -v2)
    for _ in range(n - 1):
        tot = f1(tot, -v2)
    return tot


def get_curves(ts, vrs):
    def vector_derivative(vector, t):
        v1, v2, i3 = vector
        return np.array(
            [
                dv1(v1, v2, vrs[int(100*t)]),
                dv2(v1, v2, i3),
                di3(v2)
            ])
    return spi.odeint(vector_derivative, [0, 0, 0], ts)

times = np.linspace(0, 10, 1000)[:-1]
vr = test.get()
curves = get_curves(times, vr)
v1_curve = curves[:, 0]
v2_curve = curves[:, 1]
i3_curve = curves[:, 2]
plt.plot(times,  v1_curve, label="v1")
plt.plot(times,  v2_curve, label="v2")
plt.plot(times,  i3_curve, label="i3")
p_curve = [p(y(v1_curve[t], vr[t]), v2_curve[t]) for t in range(999)]
plt.plot(times, p_curve, label="p")

plt.show()


