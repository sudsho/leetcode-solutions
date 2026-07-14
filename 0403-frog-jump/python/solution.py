from typing import List


class Solution:
    def canCross(self, stones: List[int]) -> bool:
        """Can the frog reach the last stone?

        State is (stone position, last jump size k). From a stone it may jump
        k-1, k, or k+1 units forward, landing only on an actual stone. We track,
        per stone, the set of jump sizes that can arrive there, then propagate
        forward. reachable[pos] holds those k values.
        """
        stone_set = set(stones)
        if stones[1] != 1:
            return False  # first jump is forced to be exactly 1 unit

        reachable = {pos: set() for pos in stones}
        reachable[1].add(1)
        last = stones[-1]

        for pos in stones:
            for k in reachable[pos]:
                for step in (k - 1, k, k + 1):
                    if step <= 0:
                        continue
                    nxt = pos + step
                    if nxt == last:
                        return True
                    if nxt in stone_set:
                        reachable[nxt].add(step)

        return last == 1  # only the trivial two-stone [0,1] case reaches here
