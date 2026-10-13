import itertools
import random
import time
from collections import deque
from typing import List

LANES = (0, 1, 2)   # lanes 1..3 in the statement, 0..2 here; obstacles[i] == lane + 1 blocks it


def side_targets(obs, i, lane, adjacent):
    """Lanes the frog on (i, lane) can jump to sideways: free at point i, and next to it if adjacent."""
    return [m for m in LANES if m != lane and obs[i] != m + 1 and (not adjacent or abs(m - lane) == 1)]


def search(obs, jump=1, adjacent=False, mark_point=False):
    """0-1 BFS on (point, lane), forward moves cost 0 and side jumps cost jump.

    mark_point=False is the real search, every (point, lane) settled once.
    mark_point=True is 1263's one mark per box cell: the first state popped at
    a point that got there by a forward move (or the start) claims the point,
    the frog may still jump sideways inside it from there, and any later
    forward arrival at that point is refused. The lanes at one point play the
    player's component, the forward move plays the push.
    """
    n = len(obs) - 1
    done = set()
    claimed = set()
    q = deque([(0, (0, 1, True))])
    while q:
        d, (i, lane, forward) = q.popleft()
        if (i, lane) in done:
            continue
        if mark_point and forward:
            if i in claimed:
                continue
            claimed.add(i)
        done.add((i, lane))
        if i == n:
            return d
        if obs[i + 1] != lane + 1:
            q.appendleft((d, (i + 1, lane, True)))
        for m in side_targets(obs, i, lane, adjacent):
            if (i, m) not in done:
                item = (d + jump, (i, m, False))
                q.append(item) if jump else q.appendleft(item)
    return -1


def oracle(obs, jump=1, adjacent=False):
    """DP down the road with no queue and no marks: carry three lanes forward, then relax side jumps.

    Side jumps at one point are a shortest path on at most three lanes, so
    two rounds of relaxation settle them even when only adjacent lanes connect.
    """
    inf = float("inf")
    dp = [inf, 0, inf]
    for i in range(len(obs)):
        if i:
            dp = [dp[l] if obs[i] != l + 1 else inf for l in LANES]
        for _ in range(2):
            for l in LANES:
                for m in side_targets(obs, i, l, adjacent):
                    dp[m] = min(dp[m], dp[l] + jump)
    best = min(dp)
    return -1 if best == inf else best


class Solution:
    def minSideJumps(self, obstacles: List[int]) -> int:
        inf = float("inf")
        dp = [1, 0, 1]
        for o in obstacles[1:]:
            if o:
                dp[o - 1] = inf
            low = min(dp)
            dp = [inf if o == l + 1 else min(dp[l], low + 1) for l in LANES]
        return min(dp)


def all_roads(n):
    """Every road of n + 1 points with the two ends clear, 4^(n - 1) of them."""
    for mid in itertools.product(range(4), repeat=n - 1):
        yield (0,) + mid + (0,)


def random_road(rng, n, rate):
    return (0,) + tuple(rng.randint(1, 3) if rng.random() < rate else 0 for _ in range(n - 1)) + (0,)


VARIANTS = (("free walk", 0, False), ("real, cost 1", 1, False), ("adjacent only", 1, True))


def ties_at_claim(obs, jump, adjacent):
    """Whether the real search pops two forward arrivals at one point at the same cost, the case one mark refuses."""
    n = len(obs) - 1
    inf = float("inf")
    dp = [inf, 0, inf]
    for i in range(1, n + 1):
        arrive = [dp[l] if obs[i] != l + 1 else inf for l in LANES]
        finite = sorted(a for a in arrive if a < inf)
        if len(finite) > 1 and finite[0] == finite[1]:
            return True
        dp = arrive
        for _ in range(2):
            for l in LANES:
                for m in side_targets(obs, i, l, adjacent):
                    dp[m] = min(dp[m], dp[l] + jump)
    return False


if __name__ == "__main__":
    t0 = time.time()
    s = Solution()
    print("examples", s.minSideJumps([0, 1, 2, 3, 0]), s.minSideJumps([0, 1, 1, 3, 3, 0]),
          s.minSideJumps([0, 2, 1, 0, 3, 0]), "want 2 0 2")

    print("\nexhaustive, every road with clear ends")
    for n in (4, 6, 8, 9):
        for name, jump, adj in VARIANTS:
            total = off = sol_off = solvable = wrong = long = minus = 0
            by = {}
            witness = None
            for obs in all_roads(n):
                total += 1
                want = search(obs, jump, adj)
                off += oracle(obs, jump, adj) != want
                if (jump, adj) == (1, False):
                    sol_off += s.minSideJumps(list(obs)) != want
                solvable += want >= 0
                got = search(obs, jump, adj, mark_point=True)
                if got != want:
                    wrong += 1
                    long += got > want >= 0
                    minus += got < 0
                    by[got - want if got >= 0 else "-1"] = by.get(got - want if got >= 0 else "-1", 0) + 1
                    if witness is None:
                        witness = obs
            print(f"  n={n} {name:13s} {total} roads, {solvable} solvable, oracle off {off}, solution off {sol_off}, "
                  f"one mark wrong {wrong} ({long} too long, {minus} say -1) by {dict(sorted(by.items(), key=str))}")
            if witness is not None and n == 4:
                print(f"    witness {witness}: answer {search(witness, jump, adj)}, "
                      f"one mark {search(witness, jump, adj, mark_point=True)}")

    print("\nevery one-mark failure against a tie between two forward arrivals, n = 8")
    for name, jump, adj in VARIANTS:
        fail = tie = fail_tie = 0
        for obs in all_roads(8):
            bad = search(obs, jump, adj, mark_point=True) != search(obs, jump, adj)
            t = ties_at_claim(obs, jump, adj)
            fail += bad
            tie += t
            fail_tie += bad and t
        print(f"  {name:13s} failures {fail}, roads with a tie {tie}, failures with a tie {fail_tie}")

    print("\nrandom, 3000 roads at each length and obstacle rate")
    rng = random.Random(1824)
    for n in (30, 100):
        for rate in (0.2, 0.5, 0.8):
            row = []
            for name, jump, adj in VARIANTS:
                wrong = off = 0
                for _ in range(3000):
                    obs = random_road(rng, n, rate)
                    want = search(obs, jump, adj)
                    off += oracle(obs, jump, adj) != want
                    wrong += search(obs, jump, adj, mark_point=True) != want
                row.append(f"{name} {wrong} (oracle off {off})")
            print(f"  n={n:3d} rate {rate:.1f}: " + ", ".join(row))

    print("\ntime at n = 5 * 10^5, 5 roads at rate 0.5")
    roads = [list(random_road(rng, 500000, 0.5)) for _ in range(5)]
    for name, fn in (("dp", s.minSideJumps), ("0-1 bfs", search)):
        tt = time.perf_counter()
        for r in roads:
            fn(r)
        print(f"  {name:8s} {1000 * (time.perf_counter() - tt) / len(roads):.0f} ms")

    print(f"\n{time.time() - t0:.0f} s")
