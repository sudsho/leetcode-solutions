from collections import deque

class Solution:
    def racecar(self, target: int) -> int:
        seen = {(0, 1)}
        q = deque([(0, 1, 0)])
        while q:
            pos, sp, steps = q.popleft()
            if pos == target:
                return steps
            # accelerate
            np, ns = pos + sp, sp * 2
            if abs(np - target) < target and (np, ns) not in seen:
                seen.add((np, ns))
                q.append((np, ns, steps + 1))
            # reverse
            ns2 = -1 if sp > 0 else 1
            if (pos, ns2) not in seen:
                seen.add((pos, ns2))
                q.append((pos, ns2, steps + 1))
        return -1
