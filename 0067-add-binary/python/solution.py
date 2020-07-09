# revisited
class Solution:
    def addBinary(self, a, b):
        i, j = len(a) - 1, len(b) - 1
        carry = 0
        out = []
        while i >= 0 or j >= 0 or carry:
            x = int(a[i]) if i >= 0 else 0
            y = int(b[j]) if j >= 0 else 0
            s = x + y + carry
            carry = s // 2
            out.append(str(s % 2))
            i -= 1
            j -= 1
        return ''.join(reversed(out))

# optim: pass small inputs straight through above
