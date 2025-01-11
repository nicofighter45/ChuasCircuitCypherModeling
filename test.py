from math import *
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as spi

# electrical constants
C2, C1, L, G, Ga, Gb, E = 50e-9, 5.56e-9, 7.14e-3, 0.7e-3, -0.8e-3, -0.5e-3, 1

# simulation constants
n = 30
h = 0.4

def p(t):
    return np.sin(t)

def f(v):
    return Gb*v + 0.5*(Ga-Gb)*(abs(v+E) - abs(v-E))

def dv1(v1, v2, vr):
    return (G*(v2-v1) -f(vr))/C1

def dv2(v1, v2, i3):
    return (G*(v1-v2) + i3)/C2

def di3(v2):
    return -v2/L

def f1(x, k):
    #print(x + k)
    if -2*h <= x + k <= -h:
        return x+k+2*h
    if -h < x + k < h:
        return x+k
    if h <= x + k <= 2*h:
        return x+k-2*h
    raise Exception("Invalid value")

def e(p, v2):
    tot = f1(p, v2)
    for _ in range(n-1):
        tot = f1(tot, v2)
    return tot

def vr(v1, v2, p):
    return v1 - e(p, v2)

def vector_derivative(vector, t):
    v1, v2, i3 = vector
    vrvar = vr(v1, v2, p(t))
    return np.array(
    [
        dv1(v1, v2, vrvar),
        dv2(v1, v2, i3),
        di3(v2)
    ])





def get():
    times = np.linspace(0, 10, 1000)
    curves = spi.odeint(vector_derivative, [0, 0, 0], times)
    plt.plot(times, curves[:, 0], label="v1")
    plt.plot(times, curves[:, 1], label="v2")
    plt.plot(times, curves[:, 2], label="i3")
    vr_curve = [vr(v1, v2, p(t)) for t, (v1, v2, i3) in zip(times, curves)]
    plt.plot(times, vr_curve, label="vr")
    plt.show()
    return vr_curve

