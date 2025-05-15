# revisited - cleaned up
class Solution:
    def romanToInt(self, s):
        value = {'I':1,'V':5,'X':10,'L':50,'C':100,'D':500,'M':1000}
        total = 0
        n = len(s)
        for i in range(n):
            # if smaller numeral before bigger, subtract
            if i + 1 < n and value[s[i]] < value[s[i+1]]:
                total -= value[s[i]]
            else:
                total += value[s[i]]
        return total

# optim: pass small inputs straight through above

# revisit: minor renames and one early exit added
