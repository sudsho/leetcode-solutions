import random


class Solution:
    def __init__(self, nums):
        # keep the original around so reset can hand it back untouched
        self.original = list(nums)
        self.arr = list(nums)

    def reset(self):
        # restore the array to its starting configuration
        self.arr = list(self.original)
        return self.arr

    def shuffle(self):
        # fisher-yates: walk from the back, swap each slot with a random
        # index at or before it. every permutation is equally likely.
        for i in range(len(self.arr) - 1, 0, -1):
            j = random.randint(0, i)
            self.arr[i], self.arr[j] = self.arr[j], self.arr[i]
        return self.arr


# quick sanity check on the uniformity - shuffle a small array many times
# and make sure every position sees every value roughly the same amount.
if __name__ == "__main__":
    from collections import Counter

    obj = Solution([1, 2, 3])
    counts = [Counter() for _ in range(3)]
    for _ in range(30000):
        s = obj.shuffle()
        for pos, val in enumerate(s):
            counts[pos][val] += 1
    for pos, c in enumerate(counts):
        print(f"position {pos}: {dict(sorted(c.items()))}")
    print("reset ->", obj.reset())
