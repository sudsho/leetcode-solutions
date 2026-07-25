class NumArray:
    def __init__(self, nums):
        # prefix[i] = sum of the first i elements, so prefix[0] = 0.
        # the leading zero is what lets sumRange(0, j) avoid a special case.
        self.prefix = [0] * (len(nums) + 1)
        for i, v in enumerate(nums):
            self.prefix[i + 1] = self.prefix[i] + v

    def sumRange(self, left, right):
        # sum(left..right) = (sum of first right+1) - (sum of first left).
        # both endpoints inclusive, hence right + 1 on the upper term.
        return self.prefix[right + 1] - self.prefix[left]
