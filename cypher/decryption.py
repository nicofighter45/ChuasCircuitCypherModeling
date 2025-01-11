from cypher.simulation import *

class Decryption(Simulation):
    def __init__(self, vr_list, times):
        super().__init__(v1_0_dec, v2_0_dec, i3_0_dec, times)
        self.vr_list = vr_list

    def p(self, v1, v2, t):
        tot = f1(self.e(t, v1), -v2)
        for _ in range(n - 1):
            tot = f1(tot, -v2)
        return tot

    def vr(self, t, _=0, __=0):
        return self.vr_list[get_k_from_t(t)]

    # encryption rule
    def e(self, t, v1):
        return v1 - self.vr(t)

    def p_list(self, solved_simulation):
        p_list = []
        for t in self.times:
            k = get_k_from_t(t)
            p_list.append(self.p(solved_simulation[0][k], solved_simulation[1][k], t))
        return np.array(p_list)
