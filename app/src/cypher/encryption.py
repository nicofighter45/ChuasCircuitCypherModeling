from app.src.abstract.simulation import *

class Encryption(Simulation):
    def __init__(self, function, times):
        self.function = function
        super().__init__(v1_0, v2_0, i3_0, times)

    def p(self, t):
        return self.function(t)

    def p_list(self):
        return np.array([self.p(t) for t in self.times])

    def vr(self, t, v1, v2):
        return v1 - self.e(t, v2)

    # encryption rule
    def e(self, t, v2):
        tot = f1(self.p(t), v2)
        for i in range(n - 1):
            tot = f1(tot, v2)
        return tot

    def vr_list(self):
        vr_list = []
        for t in self.times:
            k = get_k_from_t(t)
            vr_list.append(self.vr(t, self.solution.y[0][k], self.solution.y[1][k]))
        return np.array(vr_list)

    def continuous_vr(self, t):
        return self.vr(t, self.solution.sol(t)[0], self.solution.sol(t)[1])

    def e_list(self):
        list = []
        for t in self.times:
            k = get_k_from_t(t)
            list.append(self.e(t, self.solution.y[1][k]))
        return np.array(list)
