from collections import defaultdict, deque
from typing import Dict, List, Tuple


def oracle(s: str, lo: int, hi: int) -> Tuple[List[int], List[int]]:
    """Distances and shortest-sequence counts, from the whole edge list.

    `O(n * hi)` edges, no window and no pointer. Counts are an explicit dp over
    the finished distances rather than being accumulated during the search, so
    nothing about visiting order can leak into them.
    """
    n = len(s)
    dist = [-1] * n
    dist[0] = 0
    queue = deque([0])
    while queue:
        i = queue.popleft()
        for j in range(i + lo, min(i + hi, n - 1) + 1):
            if s[j] == "0" and dist[j] < 0:
                dist[j] = dist[i] + 1
                queue.append(j)

    ways = [0] * n
    ways[0] = 1
    for j in sorted(range(1, n), key=lambda k: dist[k]):
        if dist[j] > 0:
            ways[j] = sum(
                ways[i]
                for i in range(max(0, j - hi), j - lo + 1)
                if dist[i] == dist[j] - 1
            )
    return dist, ways


def scan(s: str, lo: int, hi: int, skip: bool = True) -> Tuple[List[int], List[int], int]:
    """The level scan, instrumented, with the `farthest` skip switchable.

    Returns `(dist, ways, scanned)`. The first-reach branch is all reachability
    needs; the `elif` is the counting program's one extra line, and it is the
    thing a skipped rescan would have reached. `scanned` counts every index the
    window loop looks at, whatever it finds there.
    """
    n = len(s)
    dist = [-1] * n
    ways = [0] * n
    dist[0] = 0
    ways[0] = 1
    queue = deque([0])
    farthest = 0
    scanned = 0
    while queue:
        i = queue.popleft()
        start = max(i + lo, farthest + 1) if skip else i + lo
        for j in range(start, min(i + hi, n - 1) + 1):
            scanned += 1
            if s[j] != "0":
                continue
            if dist[j] < 0:
                dist[j] = dist[i] + 1
                ways[j] = ways[i]
                queue.append(j)
            elif dist[j] == dist[i] + 1:
                ways[j] += ways[i]
        if skip:
            farthest = i + hi
    return dist, ways, scanned


def count_by_level_runs(s: str, lo: int, hi: int) -> int:
    """Shortest-sequence count in `O(n)`, keeping the skip.

    Leans on the distances being non-decreasing in the index, which the skipped
    scan gets for free - it pushes in increasing index order, and a bfs queue is
    in level order - and which `__main__` asserts rather than trusts. So level L
    is one contiguous run of reachable indices, and the predecessors of `j` that
    sit one level down are a window intersected with that run: one prefix-sum
    difference.
    """
    n = len(s)
    dist, _, _ = scan(s, lo, hi, skip=True)
    first: Dict[int, int] = {}
    last: Dict[int, int] = {}
    for k, d in enumerate(dist):
        if d >= 0:
            first.setdefault(d, k)
            last[d] = k

    ways = [0] * n
    prefix = [0] * (n + 1)
    ways[0] = 1
    prefix[1] = 1
    for j in range(1, n):
        if dist[j] > 0:
            level = dist[j] - 1
            a = max(j - hi, first[level])
            b = min(j - lo, last[level])
            if a <= b:
                ways[j] = prefix[b + 1] - prefix[a]
        prefix[j + 1] = prefix[j] + ways[j]
    return ways[n - 1]


def count_min_jumps_1345(arr: List[int], clear_groups: bool) -> int:
    """1345's bfs with the counting `elif` added, bucket clear switchable.

    The neighbours of `i` are a set, because `i + 1` can also be in the bucket
    and a jump sequence is a sequence of indices, not of edge kinds.
    """
    n = len(arr)
    by_value: Dict[int, List[int]] = defaultdict(list)
    for i, value in enumerate(arr):
        by_value[value].append(i)
    dist = [-1] * n
    ways = [0] * n
    dist[0] = 0
    ways[0] = 1
    queue = deque([0])
    while queue:
        i = queue.popleft()
        neighbours = set(by_value[arr[i]])
        neighbours.update((i - 1, i + 1))
        neighbours.discard(i)
        if clear_groups:
            by_value[arr[i]].clear()
        for j in neighbours:
            if not 0 <= j < n:
                continue
            if dist[j] < 0:
                dist[j] = dist[i] + 1
                ways[j] = ways[i]
                queue.append(j)
            elif dist[j] == dist[i] + 1:
                ways[j] += ways[i]
    return ways[n - 1]


def oracle_1345(arr: List[int]) -> int:
    n = len(arr)
    adjacent = [
        {j for j in range(n) if j != i and (arr[j] == arr[i] or abs(i - j) == 1)}
        for i in range(n)
    ]
    dist = [-1] * n
    dist[0] = 0
    queue = deque([0])
    while queue:
        i = queue.popleft()
        for j in adjacent[i]:
            if dist[j] < 0:
                dist[j] = dist[i] + 1
                queue.append(j)
    ways = [0] * n
    ways[0] = 1
    for j in sorted(range(1, n), key=lambda k: dist[k]):
        ways[j] = sum(ways[i] for i in adjacent[j] if dist[i] == dist[j] - 1)
    return ways[n - 1]


class Solution:
    def canReach(self, s: str, minJump: int, maxJump: int) -> bool:
        """Whether index n-1 is reachable from 0, jumping forward between
        `minJump` and `maxJump` and landing only on '0'.

        Taken for the 11th's open item. 882's table says a deleted guard is safe
        exactly when every update it lets a repeat reach absorbs the repeat, and
        1345's bucket clear only ever skips a rescan that reaches
        `if not visited[j]`, which absorbs. The table's prediction was that
        counting shortest sequences reverses it: a second member reaching the
        same next-level index brings ways the first did not, so keeping the
        clear is the bug and deleting it is the fix.

        Counting shortest jump sequences in 1345 is not a problem on the site.
        This one is the nearest thing that is, because its standard solution
        has the same line in a different shape - `farthest`, the right end of
        the last window scanned, and each new window starts past it. It never
        changes an answer: everything in `[i + minJump, farthest]` was scanned
        by an earlier, lower index, and visited or rejected there. And it is
        the whole bound, `n - 1` against `n(n - 1)/2` on all zeros with the
        widest window. Both measured in `__main__`, and 1345's clear under
        counting is run there too, so the prediction is checked on the line it
        was made about and not only on its neighbour.
        """
        n = len(s)
        if s[-1] != "0":
            return False
        reached = [False] * n
        reached[0] = True
        queue = deque([0])
        farthest = 0
        while queue:
            i = queue.popleft()
            if i == n - 1:
                return True
            # everything up to farthest was already scanned from a lower index.
            # deleting this leaves every answer alone and makes it n * maxJump.
            for j in range(max(i + minJump, farthest + 1), min(i + maxJump, n - 1) + 1):
                if s[j] == "0" and not reached[j]:
                    reached[j] = True
                    queue.append(j)
            farthest = i + maxJump
        return False


if __name__ == "__main__":
    import itertools
    import random

    solution = Solution()

    cases: List[Tuple[str, int, int, bool]] = [
        ("011010", 2, 3, True),
        ("01101110", 2, 3, False),
        ("00", 1, 1, True),
        ("0000000001", 1, 9, False),
        ("0111110", 6, 6, True),
    ]
    print("answers")
    for text, lo, hi, expected in cases:
        got = solution.canReach(text, lo, hi)
        assert got == expected == (oracle(text, lo, hi)[0][-1] >= 0), (text, lo, hi, got)
        print(f"  s={text!r:14s} lo={lo} hi={hi}  {got}")

    # every string of length 2..12 starting with '0', every 1 <= lo <= hi < n.
    print("\nskip vs no skip, exhaustively, reach and count")
    instances = stale_sensitive = skip_count_wrong = 0
    for n in range(2, 13):
        for tail in itertools.product("01", repeat=n - 1):
            text = "0" + "".join(tail)
            for lo in range(1, n):
                for hi in range(lo, n):
                    dist, ways = oracle(text, lo, hi)
                    d_skip, w_skip, _ = scan(text, lo, hi, skip=True)
                    d_plain, w_plain, _ = scan(text, lo, hi, skip=False)
                    assert d_skip == d_plain == dist, (text, lo, hi)
                    assert solution.canReach(text, lo, hi) == (dist[-1] >= 0)
                    reachable = [d for d in dist if d >= 0]
                    assert reachable == sorted(reachable), (text, lo, hi)
                    assert w_plain == ways, (text, lo, hi)
                    assert count_by_level_runs(text, lo, hi) == ways[-1], (text, lo, hi)
                    # under the skip every index is scanned once, by its lowest
                    # predecessor, so the count copies 1 down the whole chain.
                    assert all(w == (1 if d >= 0 else 0) for w, d in zip(w_skip, dist))
                    instances += 1
                    if dist[-1] >= 0:
                        stale_sensitive += 1
                        if w_skip[-1] != ways[-1]:
                            skip_count_wrong += 1
                            assert lo < hi
    print(f"  {instances} instances, reach and dist identical with and without the skip")
    print(f"  reachable {stale_sensitive}   skip + counting wrong {skip_count_wrong}"
          f"   no skip + counting wrong 0   level-run counter wrong 0")

    print("\ncost of dropping the skip, on '0' * n with the widest window")
    for n in (10, 50, 200, 800, 2000):
        text = "0" * n
        _, _, kept = scan(text, 1, n - 1, skip=True)
        _, _, dropped = scan(text, 1, n - 1, skip=False)
        assert kept == n - 1 and dropped == n * (n - 1) // 2, (n, kept, dropped)
        print(f"  n={n:5d}  skip={kept:6d} (n-1)   no skip={dropped:8d} (n(n-1)/2)"
              f"   ratio={dropped / kept:7.1f}")

    random.seed(12)
    print("\nno skip / skip on random strings, n = 2000, 70% zeros, by window width")
    for width in (1, 2, 5, 20, 100, 500):
        ratios = []
        for _ in range(5):
            text = "0" + "".join("0" if random.random() < 0.7 else "1" for _ in range(1999))
            _, _, kept = scan(text, 1, width, skip=True)
            _, _, dropped = scan(text, 1, width, skip=False)
            ratios.append(dropped / kept)
        print(f"  lo=1 hi={width:4d}   ratio={sum(ratios) / len(ratios):8.2f}x")

    print("\nskip + counting on random strings, n = 40, 70% zeros")
    for lo, hi in ((3, 3), (2, 3), (2, 4), (3, 7), (1, 10)):
        reachable = wrong = slack = 0
        for _ in range(400):
            text = "0" + "".join("0" if random.random() < 0.7 else "1" for _ in range(39))
            dist, ways = oracle(text, lo, hi)
            if dist[-1] < 0:
                continue
            reachable += 1
            wrong += scan(text, lo, hi, skip=True)[1][-1] != ways[-1]
            # how far the shortest sequences could overshoot 39 if every jump
            # were maximal. zero slack means one sequence and nothing to lose.
            slack += dist[-1] * hi - 39
        mean_slack = slack / reachable if reachable else 0.0
        print(f"  lo={lo} hi={hi:2d}   reachable {reachable:3d}/400   skip + counting wrong {wrong:3d}"
              f"   mean slack {mean_slack:5.2f}")

    print("\n1345's bucket clear under counting, exhaustively")
    for alphabet, length in ((2, 10), (3, 7)):
        total = wrong_cleared = 0
        for values in itertools.product(range(alphabet), repeat=length):
            values = list(values)
            truth = oracle_1345(values)
            assert count_min_jumps_1345(values, clear_groups=False) == truth, values
            total += 1
            wrong_cleared += count_min_jumps_1345(values, clear_groups=True) != truth
        print(f"  |values|={alphabet} length={length}  {total} arrays"
              f"   cleared wrong {wrong_cleared}   uncleared wrong 0")

    print("\nsame, random arrays of length 60")
    for distinct in (60, 20, 8, 3):
        wrong_cleared = one_jump = 0
        for _ in range(300):
            values = [random.randrange(distinct) for _ in range(60)]
            truth = oracle_1345(values)
            assert count_min_jumps_1345(values, clear_groups=False) == truth
            wrong = count_min_jumps_1345(values, clear_groups=True) != truth
            wrong_cleared += wrong
            # ends sharing a value is one jump and exactly one sequence.
            if values[0] == values[-1]:
                one_jump += 1
                assert truth == 1 and not wrong
        print(f"  |distinct values|={distinct:3d}   cleared wrong {wrong_cleared:3d}/300"
              f"   of the {300 - one_jump:3d} not solved in one jump")
