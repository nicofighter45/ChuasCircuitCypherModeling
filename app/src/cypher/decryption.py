from app.src.abstract.simulation import *

class Decryption(Simulation):
    """Decryption implementation"""
    def __init__(self, encryptor, times):
        self.__encryptor = encryptor
        super().__init__(v1_0_dec, v2_0_dec, i3_0_dec, times)

    def __p(self, t, v1, v2):
        tot = f1(self.e(t, v1), -v2)
        for _ in range(n - 1):
            tot = f1(tot, -v2)
        return tot

    def vr(self, t, _=0, __=0):
        k = get_k_from_t(t)
        return self.__encryptor.vr(t, self.__encryptor.solution.y[0][k], self.__encryptor.solution.y[1][k])

    # encryption rule
    def e(self, t, v1):
        return v1 - self.vr(t)

    def p_list(self):
        p_list = []
        for t in self._times:
            k = get_k_from_t(t)
            p_list.append(self.__p(t, self.solution.y[0][k], self.solution.y[1][k]))
        return np.array(p_list)

    def continuous_p(self, t):
        return self.__p(t, self.solution.sol(t)[0], self.solution.sol(t)[1])
