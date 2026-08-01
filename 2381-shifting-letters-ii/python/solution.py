class Solution:
    def shiftingLetters(self, s, shifts):
        # difference array over the string's own indices. the thing that makes
        # this one click is that shifts COMPOSE additively - shifting forward 3
        # then back 1 is the same as forward 2 - so a pile of overlapping range
        # updates collapses into a single net shift per position. if the
        # operation weren't commutative and additive the whole technique would
        # be unavailable and the order of shifts would matter.
        n = len(s)
        diff = [0] * (n + 1)  # +1 so a shift ending at n - 1 closes in-bounds

        for start, end, direction in shifts:
            amount = 1 if direction == 1 else -1
            # inclusive range, so the cancel lands at end + 1. unlike 1094's
            # half-open drop-offs, end really is still shifted here.
            diff[start] += amount
            diff[end + 1] -= amount

        # accumulate into the net shift for each position and apply it. the net
        # can be large in either direction (up to +/- len(shifts)), so the mod
        # is doing real work, not just wrapping z -> a on the boundary.
        result = []
        running = 0
        for i in range(n):
            running += diff[i]
            # python's % is already non-negative for a positive modulus, so
            # -3 % 26 == 23 and backward shifts wrap without a guard. worth
            # flagging: in java or c++ this line needs ((x % 26) + 26) % 26,
            # same footgun as the remainder buckets in 974.
            offset = (ord(s[i]) - ord("a") + running) % 26
            result.append(chr(ord("a") + offset))

        return "".join(result)

    def shiftingLettersNaive(self, s, shifts):
        """The O(n * m) version, kept to show what the diff array is replacing.

        Walks every index of every shift range. Correct, and the reason the
        problem has the constraints it does - with n and m both up to 5 * 10^4
        this is 2.5 billion character updates.
        """
        net = [0] * len(s)

        for start, end, direction in shifts:
            amount = 1 if direction == 1 else -1
            for i in range(start, end + 1):
                net[i] += amount

        return "".join(
            chr(ord("a") + (ord(c) - ord("a") + net[i]) % 26)
            for i, c in enumerate(s)
        )
