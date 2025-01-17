import numpy as np
from scipy.optimize import root
from matplotlib import pyplot as plt
from math import pi

from app.src.cypher.decryption import Decryption
from app.src.cypher.encryption import Encryption
from app.src.constants import *


class Manager:
    def __init__(self, f, function):
        self.times = np.array([i * end / number for i in range(number)])
        self.encryption = Encryption(lambda t: function(t, f, 0, 0), self.times)
        self.decryption = Decryption(self.encryption, self.times)
        self.initial_p = self.encryption.p_list()
        self.vr = self.encryption.vr_list()
        self.final_p = self.decryption.p_list()
        self.function = function
        self.fp = 0
        self.fr = 0

    def export_graphs(self):
        fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
        fig.patch.set_facecolor((BACKGROUND_COLOR[0]/255, BACKGROUND_COLOR[1]/255, BACKGROUND_COLOR[2]/255))
        ax1.set_title("Vr(t) public shared encrypted message (for last character)")
        ax1.set_ylabel("Volt (V)")
        ax1.set_xlabel("Time (ms)")
        ax1.xaxis.set_label_coords(-0.07, -0.05)
        ax1.plot(self.times * 1000, self.vr, label="vr", color='orange')
        ax2.set_ylabel("Volt (V)")
        ax2.plot(self.times*1000, self.final_p, label="d")
        ax2.plot(self.times*1000, self.initial_p, label="p")
        ax2.xaxis.tick_top()
        handles, labels = ax2.get_legend_handles_labels()
        ax2.legend(handles[::-1], labels[::-1], loc="lower right")
        fig.text(0.5, 0.05, "p(t) initial message and d(t) decrypted message (for last character)",
                 ha='center', fontsize=12)
        fig.savefig('app/ressources/graph.png')


    def curve_fit(self):

        final_p_zeros, vr_zeros = [], []
        t = end/2
        while t < end:
            if abs(self.decryption.continuous_p(t)) < 0.1:
                t0 = root(self.decryption.continuous_p, t).x[0]
                final_p_zeros.append(t0*1000)
                t += 5e-4
            t += end/number
        t = end/2
        while t < end:
            if abs(self.encryption.continuous_vr(t)) < 0.1:
                t0 = root(self.encryption.continuous_vr, t).x[0]
                vr_zeros.append(t0*1000)
                t += 5e-4
            else:
                t += end/number
        self.fp = int(round(pi/(np.median(np.diff(final_p_zeros))), 2)*1000)
        self.fr = int(round(pi/(np.median(np.diff(vr_zeros))), 2)*1000)
