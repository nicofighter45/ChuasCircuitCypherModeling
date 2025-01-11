from cypher.simulation import *

class Decryption(Simulation):
    def __init__(self, vr_list):
        super().__init__(v1_0_dec, v2_0_dec, i3_0_dec)
        self.vr_list = vr_list

    def p(self):
        tot = f1(self.e(), -self.v2)
        for _ in range(n - 1):
            tot = f1(tot, -self.v2)
        return tot

    def vr(self):
        return self.vr_list[get_k_from_t(self.t)]

    # encryption rule
    def e(self):
        return self.v1 - self.vr()

    def p_list(self, solved_simulation):
        p_list = []
        for t_local in self.times:
            self.t = t_local
            k = get_k_from_t(self.t)
            self.v1 = solved_simulation[0][k]
            self.v2 = solved_simulation[1][k]
            self.i3 = solved_simulation[2][k]
            p_list.append(self.p())
        return np.array(p_list)
