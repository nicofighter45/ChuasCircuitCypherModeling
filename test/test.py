from cypher.decryption import *
from cypher.encryption import *
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import time


def function_to_encrypt(t):
    return np.sin(4100*t)

timenow = time.time()
encryption = Encryption(function_to_encrypt)
initial_p = encryption.p_list
simu_encryption = encryption.solve()
vr = encryption.vr_list(simu_encryption)
decryption = Decryption(vr)
simu_decryption = decryption.solve()
final_p = decryption.p_list(simu_decryption)
times = decryption.times
print(time.time() - timenow)

encryption.print_simulation_result(simu_encryption, "encryption")
decryption.print_simulation_result(simu_decryption, "encryption")
plt.title("Simulation global")
plt.plot(times, initial_p, label="p")
plt.plot(times, final_p, label="final p")
plt.plot(times, vr, label="vr")
plt.axis([0, end, -5, 5])
plt.legend(["p", "final p", "vr (V)"])
plt.show()
plt.plot(times, vr, label="vr")
plt.show()

print(curve_fit(lambda t, a, b: np.sin(a*t-b), times[int(number/2):], final_p[int(number/2):], p0=[4000, 0])[0][0])
print(curve_fit(lambda t, a, b: np.sin(a*t-b), times[int(number/2):], vr[int(number/2):], p0=[4000, 0])[0][0])
