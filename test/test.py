from cypher.decryption import *
from cypher.encryption import *
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import time


def th_function(t, A, B, C):
    return 0.4*np.sin(A*t-B)+C


def show_main():
    plt.title("Simulation global " + str(f) + "Hz")
    plt.plot(times, initial_p, label="p")
    plt.plot(times, final_p, label="final p")
    plt.legend(["p", "final p"])
    plt.show()
    plt.plot(times, vr, label="vr")
    plt.show()
    plt.plot(times, ept, label="e(p(t))")
    plt.show()
    #plt.axis([0, end, -0.4, 0.4])
    #plt.legend(["p", "final p", "vr (V), e(p(t))"])


def show():
    encryption.print_simulation_result(simu_encryption, "encryption")
    decryption.print_simulation_result(simu_decryption, "decryption")
    show_main()


times = np.array([i * end / number for i in range(number)])
for f in range(3000, 3350, 10000):
    def function_to_encrypt(t):
        return th_function(t, f, 0, 0)
    timenow = time.time()
    encryption = Encryption(function_to_encrypt, times)
    initial_p = encryption.p_list()
    simu_encryption = encryption.solve()
    vr = encryption.vr_list(simu_encryption)
    ept = encryption.e_list(simu_encryption)
    decryption = Decryption(vr, times)
    simu_decryption = decryption.solve()
    final_p = decryption.p_list(simu_decryption)
    fit_p_values = curve_fit(th_function, times[int(number / 2):], final_p[int(number / 2):], p0=[3200, 0, 0])[0]
    fit_p = int(1000 * round(fit_p_values[0] / 1000, 2))
    fit_vr_values = curve_fit(th_function, times[int(number / 2):], final_p[int(number / 2):], p0=[3200, 0, 0])[0]
    fit_vr = int(1000 * round(fit_vr_values[0] / 1000, 2))

    show_main()
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
