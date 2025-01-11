from cypher.simulation import *

class Encryption(Simulation):
    def __init__(self, function):
        super().__init__(v1_0, v2_0, i3_0)
        self.p_list = np.array([function(t) for t in self.times])

    def p(self):
        return self.p_list[get_k_from_t(self.t)]

    def vr(self):
        return self.v1 - self.e()

    # encryption rule
    def e(self):
        tot = f1(self.p(), self.v2)
        for _ in range(n - 1):
            tot = f1(tot, self.v2)
        return tot

    def vr_list(self, solved_simulation):
        vr_list = []
        for t_local in self.times:
            self.t = t_local
            k = get_k_from_t(self.t)
            self.v1 = solved_simulation[0][k]
            self.v2 = solved_simulation[1][k]
            self.i3 = solved_simulation[2][k]
            vr_list.append(self.vr())
        return np.array(vr_list)
