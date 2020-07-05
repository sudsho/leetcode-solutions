# minor pass
class Solution:
    def isPalindrome(self, x):
        # negative numbers cannot be palindromes (the - sign messes it up)
        if x < 0:
            return False
        s = str(x)
        return s == s[::-1]

# optim: pass small inputs straight through above
