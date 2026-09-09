from collections import defaultdict, deque
from typing import Dict, List, Tuple


def brute_force_steps(arr: List[int]) -> int:
    """Minimum jumps, by building the whole graph and walking it.

    `O(n^2)` edges and not used by the solution. The oracle's job on the last
    three nights kept turning out to be something other than what it was written
    for; here it is written for exactly one thing, which is to certify that the
    guard being measured below never changes an answer.
    """
    n = len(arr)
    adjacent: Dict[int, List[int]] = {i: [] for i in range(n)}
    by_value: Dict[int, List[int]] = defaultdict(list)
    for i, value in enumerate(arr):
        by_value[value].append(i)
    for i in range(n):
        if i > 0:
            adjacent[i].append(i - 1)
        if i + 1 < n:
            adjacent[i].append(i + 1)
        for j in by_value[arr[i]]:
            if j != i:
                adjacent[i].append(j)

    distance = [-1] * n
    distance[0] = 0
    queue = deque([0])
    while queue:
        i = queue.popleft()
        for j in adjacent[i]:
            if distance[j] < 0:
                distance[j] = distance[i] + 1
                queue.append(j)
    return distance[n - 1]


def bfs(arr: List[int], clear_groups: bool = True) -> Tuple[int, int]:
    """The level-order scan, instrumented, with the bucket clear switchable.

    Returns `(steps, candidates_scanned)`. `candidates_scanned` counts every
    neighbour the loop looks at, visited or not, which is the quantity the
    `O(n)` claim is about - the answer itself is identical either way.

    `clear_groups=False` is the version that leaves `by_value[arr[i]]` in place
    after expanding it, which is the line whose cost is measured in `__main__`.
    """
    n = len(arr)
    if n == 1:
        return 0, 0

    by_value: Dict[int, List[int]] = defaultdict(list)
    for i, value in enumerate(arr):
        by_value[value].append(i)

    visited = [False] * n
    visited[0] = True
    frontier = deque([0])
    steps = 0
    scanned = 0

    while frontier:
        for _ in range(len(frontier)):
            i = frontier.popleft()
            if i == n - 1:
                return steps, scanned
            same = by_value[arr[i]]
            scanned += len(same)
            for j in same:
                if not visited[j]:
                    visited[j] = True
                    frontier.append(j)
            if clear_groups:
                same.clear()
            for j in (i - 1, i + 1):
                scanned += 1
                if 0 <= j < n and not visited[j]:
                    visited[j] = True
                    frontier.append(j)
        steps += 1
    return -1, scanned


class Solution:
    def minJumps(self, arr: List[int]) -> int:
        """Fewest jumps from index 0 to index n-1, moving to i-1, i+1, or any
        index holding the same value.

        Picked to test the position the 7th left open and refused to promote.
        That night's finding was a line - `i = max(i + k + 1, j)` in the suffix
        duel - that no part of the correctness argument mentions and that is
        nevertheless the entire complexity bound: exactly `n` steps against
        exactly `n^2 / 4 - 1` on a family where both versions agree about the
        answer at every size. 685 and 499 were both about conventions that
        decide the printed answer. This was a third thing and it had one
        instance, found in a two-pointer scan on strings, which is the same
        setting the axis it came from was born in.

        So the question tonight is whether that position survives a change of
        algorithm family, and this is about as far from a lex duel as the log
        goes: unweighted BFS on a graph with `O(n^2)` edges that is never built.

        The graph is index `i` joined to `i - 1`, `i + 1`, and every `j` with
        `arr[j] == arr[i]`. The value classes are what make it dense - one class
        of size `m` contributes `m(m-1)` edges - so the scan holds them as
        buckets and expands a whole bucket in one step.

        `same.clear()` is the line. When `i` is dequeued, every index in its
        value class is enqueued right there or was already visited, so the class
        is exhausted the first time any member of it is expanded and every later
        look at that bucket finds nothing to do. Deleting it is therefore a
        no-op for the visited set, which is a one-line argument, and the answer
        cannot move.

        Necessity is the other direction and it is not one line. `[7] * n` puts
        every index in one class of size `n`; without the clear each of the `n`
        dequeues rescans all `n` of them and the scan is quadratic while
        returning `1`. Measured in `__main__`.

        Note the asymmetry against the 7th, because it is the part I did not
        expect. There, harmlessness was the subtle direction - dropping the max
        is safe only because everything below `j` died in an earlier round - and
        it took an exhaustive search to believe. Here harmlessness is immediate
        and necessity is the whole story. Same position, opposite proof
        obligations, so what the two nights share is the position and not the
        difficulty of getting into it.

        And the two are not equally easy to miss. The 7th's max needed a
        periodic string before it cost anything and random inputs never found
        it; this one needs one repeated value, and a random array over 100
        values already pays 6x. Also measured in `__main__`.
        """
        n = len(arr)
        if n == 1:
            return 0

        by_value: Dict[int, List[int]] = defaultdict(list)
        for i, value in enumerate(arr):
            by_value[value].append(i)

        visited = [False] * n
        visited[0] = True
        frontier = deque([0])
        steps = 0

        while frontier:
            for _ in range(len(frontier)):
                i = frontier.popleft()
                if i == n - 1:
                    return steps
                same = by_value[arr[i]]
                for j in same:
                    if not visited[j]:
                        visited[j] = True
                        frontier.append(j)
                # the whole class is settled by this one expansion, so the
                # bucket has nothing left to offer anyone. dropping this leaves
                # every answer unchanged and makes the scan quadratic - it is
                # the O(n) bound and no part of the correctness argument sees it.
                same.clear()
                for j in (i - 1, i + 1):
                    if 0 <= j < n and not visited[j]:
                        visited[j] = True
                        frontier.append(j)
            steps += 1
        return -1


if __name__ == "__main__":
    import itertools
    import random

    solution = Solution()

    cases: List[Tuple[List[int], int]] = [
        ([100, -23, -23, 404, 100, 23, 23, 23, 3, 404], 3),
        ([7], 0),
        ([7, 6, 9, 6, 9, 6, 9, 7], 1),
        ([6, 1, 9], 2),
        ([11, 22, 7, 7, 7, 7, 7, 7, 7, 22, 13], 3),
        ([7, 7, 7, 7, 7, 7, 7, 7, 7], 1),
    ]
    print("answers, and the candidates the scan looked at to get them")
    for values, expected in cases:
        got = solution.minJumps(values)
        steps, scanned = bfs(values)
        assert got == expected == steps, (values, got, expected, steps)
        assert got == brute_force_steps(values), (values, got)
        print(f"  n={len(values):3d}  answer={got}  scanned={scanned:4d}")

    # the clear is answer-preserving, and unlike the 7th's max this direction is
    # a one-line argument. asserted anyway, over every array on 2 and 3 values.
    print("\nclear vs no clear, exhaustively")
    for alphabet, length in ((2, 11), (3, 8)):
        checked = 0
        for values in itertools.product(range(alphabet), repeat=length):
            values = list(values)
            guarded, _ = bfs(values, clear_groups=True)
            plain, _ = bfs(values, clear_groups=False)
            assert guarded == plain == brute_force_steps(values), values
            checked += 1
        print(f"  |values|={alphabet}  length={length}  {checked} arrays, no disagreement")

    # and it is the entire bound. one value class of size n, answer 1 either
    # way, and both counts are exact rather than asymptotic: 3n - 2 against
    # n^2 + n - 2, checked as an identity at every size below.
    print("\ncost of dropping the clear, on [7] * n")
    for n in (10, 50, 200, 800, 2000):
        values = [7] * n
        guarded_steps, guarded_scan = bfs(values, clear_groups=True)
        plain_steps, plain_scan = bfs(values, clear_groups=False)
        assert guarded_steps == plain_steps == 1, n
        assert guarded_scan == 3 * n - 2, (n, guarded_scan)
        assert plain_scan == n * n + n - 2, (n, plain_scan)
        print(
            f"  n={n:5d}  cleared={guarded_scan:6d} (3n-2)"
            f"   uncleared={plain_scan:8d} (n^2+n-2)"
            f"   ratio={plain_scan / guarded_scan:8.1f}"
        )

    # written before the run: the guard is invisible on random data, the way the
    # 7th's max was, and only shows up on a family built to expose it. that is
    # wrong, and it is the one thing tonight I had to correct. there is no
    # threshold - the penalty is the mean class size and it rises smoothly the
    # moment values start repeating, so random arrays at 100 distinct values
    # already pay 6x. the 7th's max really was invisible outside its family
    # because re-elimination needs a periodic string; this one needs only a
    # collision. same position, and it is not equally hard to find.
    random.seed(7)
    print("\nsame comparison on random arrays of length 2000, by class count")
    for distinct in (2000, 500, 100, 20, 4, 1):
        ratios = []
        for _ in range(5):
            values = [random.randrange(distinct) for _ in range(2000)]
            _, guarded_scan = bfs(values, clear_groups=True)
            _, plain_scan = bfs(values, clear_groups=False)
            ratios.append(plain_scan / guarded_scan)
        mean_ratio = sum(ratios) / len(ratios)
        print(f"  |distinct values|={distinct:5d}   uncleared/cleared = {mean_ratio:7.2f}x")
