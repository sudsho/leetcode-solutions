from collections import deque


class Solution:
    def minKBitFlips(self, nums, k):
        """Fewest length-k window flips to turn every bit into 1, or -1.

        Sweeping left to right, the value at index i is decided once and never
        revisited: whatever its current parity of flips is, if it still reads 0
        the *only* way to fix it is to start a fresh flip window at i (any window
        starting earlier has already passed, any starting later cannot reach i
        without also disturbing settled positions). So the greedy choice is
        forced, which is why greedy is optimal here.

        The trick is tracking the live flip parity cheaply. `flipped` is a queue
        of the start indices of windows still covering the current position; a
        window started at j stops covering i once i >= j + k, so we expire those
        from the front. The parity of the queue's length tells us the net effect
        on nums[i]: an even number of overlapping flips cancels out. When the
        effective bit (original XOR parity) is 0 we must flip - but only if a
        full k-window fits; if i + k > n we are stuck and return -1.
        """
        n = len(nums)
        flipped = deque()  # start indices of windows still affecting index i
        flips = 0
        for i in range(n):
            # drop windows whose k-length reach ended before i
            if flipped and flipped[0] + k <= i:
                flipped.popleft()
            # parity of active windows tells us the bit's current value
            effective = nums[i] ^ (len(flipped) & 1)
            if effective == 0:
                if i + k > n:
                    return -1  # no room for a window covering i
                flipped.append(i)
                flips += 1
        return flips


if __name__ == "__main__":
    s = Solution()
    assert s.minKBitFlips([0, 1, 0], 1) == 2
    assert s.minKBitFlips([1, 1, 0], 2) == -1
    assert s.minKBitFlips([0, 0, 0, 1, 0, 1, 1, 0], 3) == 3
    assert s.minKBitFlips([1, 1, 1], 2) == 0
    assert s.minKBitFlips([0], 1) == 1
    print("all good")
