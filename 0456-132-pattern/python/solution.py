class Solution:
    def find132pattern(self, nums):
        # we want i < j < k with nums[i] < nums[k] < nums[j]. scan from the RIGHT
        # keeping a monotonic-decreasing stack of candidate "2" values (the j /
        # peak). `third` is the best "k" (the middle value) we have popped so far,
        # i.e. the largest value that still had a bigger element to its right.
        # once we meet any nums[i] < third to the left, the 1-3-2 is complete.
        third = float("-inf")
        stack = []  # decreasing; holds potential peaks (the "3")

        for n in reversed(nums):
            # if the current number is below `third`, it plays the role of "1"
            # and we already have a valid 3 > 2 pair to its right -> done
            if n < third:
                return True
            # anything smaller than n on the stack can serve as the "2": pop it
            # and lift `third`, since n is a bigger element sitting to its left
            while stack and stack[-1] < n:
                third = stack.pop()
            stack.append(n)
        return False
