# 2023 nit (13)
# matrix exponentiation - log(n) version
class Solution:
    def checkRecord(self, n: int) -> int:
        MOD = 10 ** 9 + 7
        # state vector size 6 (2 * 3)
        from copy import deepcopy

        def mat_mul(A, B):
            R = [[0] * len(B[0]) for _ in range(len(A))]
            for i in range(len(A)):
                for k in range(len(B)):
                    if A[i][k] == 0:
                        continue
                    a = A[i][k]
                    for j in range(len(B[0])):
                        R[i][j] = (R[i][j] + a * B[k][j]) % MOD
            return R

        def mat_pow(M, p):
            size = len(M)
            R = [[int(i == j) for j in range(size)] for i in range(size)]
            base = deepcopy(M)
            while p:
                if p & 1:
                    R = mat_mul(R, base)
                base = mat_mul(base, base)
                p >>= 1
            return R

        # state: (a, l)  -> index 3*a + l
        # transitions:
        # +P -> (a, 0)
        # +A -> (1, 0) only if a==0
        # +L -> (a, l+1) only if l < 2
        T = [[0] * 6 for _ in range(6)]
        for a in range(2):
            for l in range(3):
                src = 3 * a + l
                # add P
                T[3 * a + 0][src] += 1
                # add A
                if a == 0:
                    T[3 * 1 + 0][src] += 1
                # add L
                if l < 2:
                    T[3 * a + (l + 1)][src] += 1

        v = [0] * 6
        v[0] = 1
        T_n = mat_pow(T, n)
        result = 0
        for r in range(6):
            for c in range(6):
                if v[c]:
                    result = (result + T_n[r][c] * v[c]) % MOD
        return result
