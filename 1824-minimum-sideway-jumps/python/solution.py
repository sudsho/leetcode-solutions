import itertools
import random
import time
from collections import deque
from typing import List

LANES = (0, 1, 2)   # lanes 1..3 in the statement, 0..2 here; obstacles[i] == lane + 1 blocks it


def side_targets(obs, i, lane, adjacent):
    """Lanes the frog on (i, lane) can jump to sideways: free at point i, and next to it if adjacent."""
    return [m for m in LANES if m != lane and obs[i] != m + 1 and (not adjacent or abs(m - lane) == 1)]


def search(obs, jump=1, adjacent=False, mark_point=False, record=None):
    """0-1 BFS on (point, lane), forward moves cost 0 and side jumps cost jump.

    mark_point=False is the real search, every (point, lane) settled once.
    mark_point=True is 1263's one mark per box cell: the first state popped at
    a point that got there by a forward move (or the start) claims the point,
    the frog may still jump sideways inside it from there, and any later
    forward arrival at that point is refused. The lanes at one point play the
    player's component, the forward move plays the push.

    record, if given, is a dict for the one-mark run: it gets each refusal as
    ((point, lane), the refused arrival's count in this run, the claimer's).
    """
    n = len(obs) - 1
    done = set()
    claimed = {}
    q = deque([(0, (0, 1, True))])
    while q:
        d, (i, lane, forward) = q.popleft()
        if (i, lane) in done:
            continue
        if mark_point and forward:
            if i in claimed:
                if record is not None:
                    record.setdefault("refused", []).append(((i, lane), d, claimed[i]))
                continue
            claimed[i] = d
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
    """A road of n + 1 points with clear ends, each inner point blocked in a uniformly drawn lane with probability rate."""
    return (0,) + tuple(rng.randint(1, 3) if rng.random() < rate else 0 for _ in range(n - 1)) + (0,)


VARIANTS = (("free walk", 0, False), ("real, cost 1", 1, False), ("adjacent only", 1, True))


def ties_at_claim(obs, jump, adjacent):
    """Whether the real search pops two forward arrivals at one point at the same cost, the case one mark refuses.

    The first version of this started the loop at point 1 and never relaxed
    the side jumps at point 0, so on the quarter of roads with lane 2 blocked
    at point 1 every count was infinite from there on and the road read as
    having no tie. That is where the "1501 of 3410" in the log came from.
    """
    n = len(obs) - 1
    inf = float("inf")
    dp = [inf, 0, inf]
    for i in range(0, n + 1):
        if i:
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


def distances(obs, jump, adjacent):
    """Every (point, lane)'s cost in the real search, the 0-1 BFS run to the end instead of stopping at point n."""
    n = len(obs) - 1
    dist = {}
    q = deque([(0, (0, 1))])
    while q:
        d, (i, lane) = q.popleft()
        if (i, lane) in dist:
            continue
        dist[(i, lane)] = d
        if i < n and obs[i + 1] != lane + 1:
            q.appendleft((d, (i + 1, lane)))
        for m in side_targets(obs, i, lane, adjacent):
            if (i, m) not in dist:
                item = (d + jump, (i, m))
                q.append(item) if jump else q.appendleft(item)
    return dist


def to_go(obs, jump, adjacent):
    """Fewest jumps from each (point, lane) to the end, the oracle's DP run backwards, inf where there is none."""
    n = len(obs) - 1
    inf = float("inf")
    rest = [None] * (n + 1)
    rest[n] = [0 if obs[n] != l + 1 else inf for l in LANES]
    for i in range(n - 1, -1, -1):
        row = [rest[i + 1][l] if obs[i] != l + 1 and obs[i + 1] != l + 1 else inf for l in LANES]
        for _ in range(2):
            for l in LANES:
                for m in side_targets(obs, i, l, adjacent):
                    row[l] = min(row[l], row[m] + jump)
        rest[i] = row
    return rest


def tie_points(obs, dist):
    """Points where the real search's cheapest forward arrival comes from two lanes at once, from its distances."""
    n = len(obs) - 1
    out = set()
    for i in range(1, n + 1):
        arrive = sorted(dist[(i - 1, l)] for l in LANES if obs[i] != l + 1 and (i - 1, l) in dist)
        if len(arrive) > 1 and arrive[0] == arrive[1]:
            out.add(i)
    return out


def refusal_study(roads, jump, adjacent, label):
    """One mark's refusals on every road, each put back on a shortest path and sorted by the tie at the claim.

    A refusal is on a shortest path when the refused state's real cost plus
    the fewest jumps from it to the end is the answer. Of those, an own tie is
    a refusal at the claimer's count in one mark's run, a real tie is a point
    the real search reaches cheapest from two lanes, and a drifted refusal is
    one whose count in one mark's run is above the state's real cost.
    """
    total = fail = refused = drift = 0
    on_path = own = own_real = own_drift = cut = 0
    witness = None
    for obs in roads:
        total += 1
        rec = {}
        got = search(obs, jump, adjacent, mark_point=True, record=rec)
        dist = distances(obs, jump, adjacent)
        n = len(obs) - 1
        want = min((dist[(n, l)] for l in LANES if (n, l) in dist), default=-1)
        refs = rec.get("refused", [])
        refused += len(refs)
        drift += sum(d > dist[st] for st, d, _ in refs)
        if got == want:
            continue
        fail += 1
        rest = to_go(obs, jump, adjacent)
        ties = tie_points(obs, dist)
        path = [(st, d, c) for st, d, c in refs if dist[st] + rest[st[0]][st[1]] == want]
        on_path += bool(path)
        tied = [(st, d, c) for st, d, c in path if d == c]
        if tied:
            own += 1
            real = any(st[0] in ties for st, _, _ in tied)
            own_real += real
            own_drift += any(d > dist[st] or c > dist[st] for st, d, c in tied)
            if witness is None and not real:
                witness = (obs, want, got, tied[0], dist[tied[0][0]])
        else:
            cut += 1
    print(f"  {label}: {total} roads, one mark wrong {fail}, refusals {refused} of which drifted {drift}; "
          f"failures with a refusal on a shortest path {on_path}, at the claimer's count {own} "
          f"(real tie at that point {own_real}, drifted count on either side {own_drift}), "
          f"above the claimer's count only {cut}")
    if witness is not None:
        obs, want, got, (st, d, c), real = witness
        print(f"    witness {obs}: answer {want}, one mark {got}; refused {st} at {d} against the claimer's {c}, "
              f"real cost {real}")


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

    # 3568 said the tie question needs the record of each refusal, own count against real cost, at the claim
    # that sits on a shortest path, and not a tie anywhere on the road; run that here on the two failing walks
    print("\nthe refusal record on the two walks that fail, each refusal put back on a shortest path")
    for n in (8, 9):
        for name, jump, adj in VARIANTS[1:]:
            refusal_study(all_roads(n), jump, adj, f"n={n} {name}")
    rng_rec = random.Random(1016)
    for n in (30, 100):
        for rate in (0.2, 0.5, 0.8):
            for name, jump, adj in VARIANTS[1:]:
                refusal_study((random_road(rng_rec, n, rate) for _ in range(3000)), jump, adj,
                              f"n={n} rate {rate:.1f} {name}")

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
