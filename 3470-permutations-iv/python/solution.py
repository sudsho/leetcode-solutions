from math import factorial

class Solution:
    def permute(self, n: int, k: int) -> list[int]:
        # alternating odd/even. Determine how to start.
        odds = [i for i in range(1, n + 1) if i % 2 == 1]
        evens = [i for i in range(1, n + 1) if i % 2 == 0]
        # number of valid permutations = 2 * (ceil(n/2)!) * (floor(n/2)!) when n even, else (ceil(n/2)!) * (floor(n/2)!)
        oc, ec = len(odds), len(evens)
        if abs(oc - ec) > 1:
            return []
        starts = []
        if oc >= ec:
            starts.append('odd')
        if ec >= oc:
            starts.append('even')
        result: list[int] = []
        odds_left = odds[:]
        evens_left = evens[:]
        # determine starting parity
        start = None
        for s in starts:
            if s == 'odd':
                count = factorial(oc) * factorial(ec)
            else:
                count = factorial(oc) * factorial(ec)
            if k <= count:
                start = s
                break
            else:
                k -= count
        if start is None:
            return []
        cur_parity = start
        for i in range(n):
            pool = odds_left if cur_parity == 'odd' else evens_left
            other = evens_left if cur_parity == 'odd' else odds_left
            # remaining slots after picking: pool has len(pool)-1 of cur, len(other) of opposite
            # number of permutations completing from each choice
            # next parity flips
            for j, x in enumerate(pool):
                # count permutations after picking x
                rest_pool = len(pool) - 1
                rest_other = len(other)
                # remaining length n-i-1 alternates starting with opposite
                remaining = factorial(rest_pool) * factorial(rest_other)
                if k <= remaining:
                    result.append(x)
                    pool.pop(j)
                    cur_parity = 'even' if cur_parity == 'odd' else 'odd'
                    break
                else:
                    k -= remaining
            else:
                return []
        return result
