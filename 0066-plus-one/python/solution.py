class Solution:
    def plusOne(self, digits):
        # walk from the right
        for i in range(len(digits) - 1, -1, -1):
            if digits[i] < 9:
                digits[i] += 1
                return digits
            digits[i] = 0
        # carried all the way - need a new leading 1
        return [1] + digits
