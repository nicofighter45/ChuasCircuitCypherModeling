from cypher.decryption import *
from cypher.encryption import *
import numpy as np
import matplotlib.pyplot as plt


encryption = Encryption(lambda t: np.sin(t*1000))
initial_p = encryption.p_list
simu_encryption = encryption.solve()
vr = encryption.vr_list(simu_encryption)
decryption = Decryption(vr)
simu_decryption = decryption.solve()
final_p = decryption.p_list(simu_decryption)
times = decryption.times

encryption.print_simulation_result(simu_encryption, "encryption")
decryption.print_simulation_result(simu_decryption, "encryption")
plt.title("Simulation global")
plt.plot(times, initial_p, label="p")
plt.plot(times, final_p, label="final p")
plt.plot(times, vr, label="vr")
plt.axis([0, 0.01, -5, 5])
plt.legend(["p", "final p", "vr (V)"])
plt.show()

