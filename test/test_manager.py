from app.src.cypher.decryption import *
from app.src.cypher.encryption import *
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import time


def th_function(t, A, B, C):
    return 0.2*np.sin(A*t-B)+C


def show_main():
    plt.title("Simulation global " + str(f) + "Hz")
    plt.plot(times, final_p)
    plt.plot(times, initial_p)
    plt.legend(["decrypt p", "p"])
    plt.show()
    plt.plot(times, vr, label="vr")
    plt.show()
    #plt.plot(times, ept, label="e(p(t))")
    #plt.show()
    #plt.axis([0, end, -0.4, 0.4])
    #plt.legend(["p", "final p", "vr (V), e(p(t))"])


def show():
    encryption.print_simulation_result("encryption")
    decryption.print_simulation_result("decryption")
    show_main()


times = np.array([i * end / number for i in range(number)])
for f in range(3300, 3350, 2000):
    def function_to_encrypt(t):
        return th_function(t, f, 0, 0)
    timenow = time.time()
    encryption = Encryption(function_to_encrypt, times)
    initial_p = encryption.p_list()
    vr = encryption.vr_list()
    ept = encryption.e_list()
    decryption = Decryption(encryption, times)
    final_p = decryption.p_list()
    fit_p_values = curve_fit(th_function, times[int(number / 2):], final_p[int(number / 2):], p0=[3200, 0, 0])[0]
    fit_p = int(1000 * round(fit_p_values[0] / 1000, 2))
    fit_vr_values = curve_fit(th_function, times[int(number / 2):], final_p[int(number / 2):], p0=[3200, 0, 0])[0]
    fit_vr = int(1000 * round(fit_vr_values[0] / 1000, 2))

    show()
    if f != fit_p:
        if f == fit_vr:
            print(f"ERROR !!! {f}Hz {time.time() - timenow}s  Guess p: {fit_p}Hz  Guess vr: {fit_vr}Hz")
        else:
            print(f"WARNING !!! {f}Hz {time.time() - timenow}s  Guess p: {fit_p}Hz  Guess vr: {fit_vr}Hz")
    else:
        if f == fit_vr:
            print(f"ATTENTION !!! {f}Hz {time.time() - timenow}s  Guess p: {fit_p}Hz  Guess vr: {fit_vr}Hz")
        else:
            print(f"{f}Hz {time.time() - timenow}s  Guess p: {fit_p}Hz  Guess vr: {fit_vr}Hz")
