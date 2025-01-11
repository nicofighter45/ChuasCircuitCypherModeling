from math import *
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as spi

# electrical constants
C2, C1, L, G, Ga, Gb, E = 50e-9, 5.56e-9, 7.14e-3, 0.7e-3, -0.8e-3, -0.5e-3, 1

# simulation constants
n = 30
h = 0.4

def f_p(t):
    return 0.3*np.sin(t)

def f_f(v):
    return Gb*v + 0.5*(Ga-Gb)*(abs(v+E) - abs(v-E))

def dv1(v1, v2, vr):
    return (G*(v2-v1) -f_f(vr))/C1

def dv2(v1, v2, i3):
    return (G*(v1-v2) + i3)/C2

def di3(v2):
    return -v2/L

def f_f1(x, k):
    if -2*h <= x + k <= -h:
        return x+k+2*h
    if -h < x + k < h:
        return x+k
    if h <= x + k <= 2*h:
        return x+k-2*h
    print(x, k, 2*h, x+k)
    raise ValueError("Invalid value")

def f_e(p, v2):
    tot = f_f1(p, v2)
    for _ in range(n-1):
        tot = f_f1(tot, v2)
    return tot

def f_vr(v1, v2, p):
    return v1 - f_e(p, v2)

def vector_derivative(vector, t):
    v1, v2, i3 = vector
    vr = f_vr(v1, v2, f_p(t))
    return np.array(
    [
        dv1(v1, v2, vr),
        dv2(v1, v2, i3),
        di3(v2)
    ])





def get():
    times = np.linspace(0, 10, 1000)
    curves = spi.odeint(vector_derivative, [-0.2, -0.02, 0.1e-3], times)
    print(curves.shape)
    plt.plot(times, curves[:, 0], label="v1")
    plt.plot(times, curves[:, 1], label="v2")
    plt.plot(times, curves[:, 2], label="i3")
    vr_curve = []
    for k in range(1000):
        vr_curve.append(f_vr(curves[:, 0][k], curves[:, 1][k], f_p(times[k])))
    plt.plot(times, vr_curve, label="vr")
    plt.show()
    return vr_curve


get()
