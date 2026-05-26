class Solution:
    def twoSum(self, numbers, target):
        # array is 1-indexed in the problem statement, sorted ascending
        lo, hi = 0, len(numbers) - 1
        while lo < hi:
            s = numbers[lo] + numbers[hi]
            if s == target:
                return [lo + 1, hi + 1]
            if s < target:
                lo += 1
            else:
                hi -= 1
        return [-1, -1]
