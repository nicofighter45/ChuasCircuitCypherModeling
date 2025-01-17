import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as spi

# electrical constants
C2, C1, L, G, Ga, Gb, E = 50e-9, 5.56e-9, 7.14e-3, 0.7e-3, -0.8e-3, -0.5e-3, 1

# simulation constants
n = 10
h = 21


def f_p(t):
    return 0.3*np.sin(1000*t)

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

def get_k_from_t(t):
    if t >= 0.01:
        return 1000 - 1
    return int(t * 1000 / 0.01)


def get():
    times = np.linspace(0, 0.01, 1000)
    curves = spi.odeint(vector_derivative, [-0.2, -0.02, 0.1e-3], times)
    v1, v2, i3 = curves[:, 0], curves[:, 1], curves[:, 2]
    plt.plot(times, 0.1*v1, label="v1")
    plt.plot(times, v2, label="v2")
    plt.plot(times, 100*i3, label="i3")
    vr_list = []
    p_list = []
    for t in times:
        k = get_k_from_t(t)
        vr_list.append(f_vr(t, v1[k], v2[k]))
        p_list.append(f_p(t))
    plt.plot(times, np.array(vr_list)/10, label="vr")
    plt.plot(times, np.array(p_list), label="p")
    plt.legend("v1 v2 i3 vr p".split())
    plt.show()


get()
