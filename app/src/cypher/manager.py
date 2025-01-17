import numpy as np
from scipy.optimize import root
from matplotlib import pyplot as plt
from math import pi

from app.src.cypher.decryption import Decryption
from app.src.cypher.encryption import Encryption
from app.src.constants import *


class Manager:
    """Manage the launch of 1 simulation"""
    def __init__(self, f, function):
        self.__times = np.array([i * end / number for i in range(number)])
        self.__encryption = Encryption(lambda t: function(t, f), self.__times)
        self.__decryption = Decryption(self.__encryption, self.__times)
        self.__initial_p = self.__encryption.p_list()
        self.__vr = self.__encryption.vr_list()
        self.__final_p = self.__decryption.p_list()
        self.fp = 0
        self.fr = 0

    def export_graphs(self, i):
        """Export the graphs of the simulation"""
        fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
        fig.patch.set_facecolor((BACKGROUND_COLOR[0]/255, BACKGROUND_COLOR[1]/255, BACKGROUND_COLOR[2]/255))
        ax1.set_title("Vr(t) public shared encrypted message (for " + str(i+1) + "th last character)")
        ax1.set_ylabel("Volt (V)")
        ax1.set_xlabel("Time (ms)")
        ax1.xaxis.set_label_coords(-0.07, -0.05)
        ax1.plot(self.__times * 1000, self.__vr, label="vr", color='orange')
        ax2.set_ylabel("Volt (V)")
        ax2.plot(self.__times * 1000, self.__final_p, label="d")
        ax2.plot(self.__times * 1000, self.__initial_p, label="p")
        ax2.xaxis.tick_top()
        handles, labels = ax2.get_legend_handles_labels()
        ax2.legend(handles[::-1], labels[::-1], loc="lower right")
        fig.text(0.5, 0.05, "p(t) initial message and d(t) decrypted message (for " + str(i+1) + "th character)",
                 ha='center', fontsize=12)
        fig.savefig('app/ressources/export/graph0' + str(i) + '.png')
        self.__encryption.print_simulation_result("encryption", 1, i)
        self.__decryption.print_simulation_result("decryption", 2, i)



    def curve_fit(self):
        """Calculate the frequency of the signal (it's not the actual frequency, it's f/2pi)"""
        final_p_zeros, vr_zeros = [], []
        t = end/2
        while t < end:
            if abs(self.__decryption.continuous_p(t)) < 0.1:
                t0 = root(self.__decryption.continuous_p, t).x[0]
                final_p_zeros.append(t0*1000)
                t += 5e-4
            t += end/number
        t = end/2
        while t < end:
            if abs(self.__encryption.continuous_vr(t)) < 0.1:
                t0 = root(self.__encryption.continuous_vr, t).x[0]
                vr_zeros.append(t0*1000)
                t += 5e-4
            else:
                t += end/number
        self.fp = int(round(pi/(np.median(np.diff(final_p_zeros))), 2)*1000)
        self.fr = int(round(pi/(np.median(np.diff(vr_zeros))), 2)*1000)
