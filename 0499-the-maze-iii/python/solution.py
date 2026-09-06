import heapq
from typing import Dict, List, Set, Tuple

# lexicographic order on the instruction letters, which is also the order the
# statement's tie-break reads. iterating the moves in this order is not what
# makes the answer lex smallest - the heap does that - but keeping the table
# sorted means the two orders never have to be reconciled by hand.
MOVES = (
    ("d", 1, 0),
    ("l", 0, -1),
    ("r", 0, 1),
    ("u", -1, 0),
)


def roll(
    maze: List[List[int]], r: int, c: int, dr: int, dc: int, hole: Tuple[int, int]
) -> Tuple[int, int, int]:
    """Roll from `(r, c)` along `(dr, dc)` until a wall or the hole stops it.

    Returns the resting cell and the number of cells travelled. The hole check
    is inside the loop rather than after it because the ball falls in when it
    passes over the hole, not when it comes to rest on it - a ball that would
    have carried on for three more cells still drops.
    """
    rows, cols = len(maze), len(maze[0])
    steps = 0
    while True:
        nr, nc = r + dr, c + dc
        if not (0 <= nr < rows and 0 <= nc < cols) or maze[nr][nc] == 1:
            return r, c, steps
        r, c, steps = nr, nc, steps + 1
        if (r, c) == hole:
            return r, c, steps


def all_optimal_paths(
    maze: List[List[int]], ball: List[int], hole: List[int]
) -> List[str]:
    """Every instruction string that reaches the hole in the minimum distance.

    Not used by the solution. It is the 685 oracle again: the answer here is a
    choice out of a set, and only the set says how large the choice is. Two
    passes - a plain Dijkstra over resting cells for the optimal distance, then
    a depth-first enumeration capped at that distance, collecting the strings
    that arrive with it exactly.

    The enumeration is exponential in the worst case and is meant for the small
    boards in `__main__`. The cap is what keeps it finite: a resting cell can be
    revisited, but only by spending distance, so no walk can cycle forever under
    a fixed budget.
    """
    start, target = (ball[0], ball[1]), (hole[0], hole[1])
    best: Dict[Tuple[int, int], int] = {}
    heap = [(0, start)]
    while heap:
        dist, cell = heapq.heappop(heap)
        if cell in best:
            continue
        best[cell] = dist
        if cell == target:
            break
        for _, dr, dc in MOVES:
            nr, nc, moved = roll(maze, cell[0], cell[1], dr, dc, target)
            if moved and (nr, nc) not in best:
                heapq.heappush(heap, (dist + moved, (nr, nc)))
    if target not in best:
        return []

    limit = best[target]
    found: Set[str] = set()

    def walk(cell: Tuple[int, int], dist: int, path: List[str]) -> None:
        if cell == target:
            if dist == limit:
                found.add("".join(path))
            return
        if dist >= limit:
            return
        for letter, dr, dc in MOVES:
            nr, nc, moved = roll(maze, cell[0], cell[1], dr, dc, target)
            if moved == 0 or dist + moved > limit:
                continue
            path.append(letter)
            walk((nr, nc), dist + moved, path)
            path.pop()

    walk(start, 0, [])
    return sorted(found)


class Solution:
    def findShortestWay(
        self, maze: List[List[int]], ball: List[int], hole: List[int]
    ) -> str:
        """Shortest roll to the hole, ties broken by lexicographically smallest
        instructions; `"impossible"` if the hole cannot be reached.

        Picked to follow up on 685 two nights ago, which is where the whole
        week's rule died. The rule was that a printed choice off a class is free
        exactly when the printed function factors through the quotient, and 685
        killed the "only if" half by producing a tie the *statement* legislated
        rather than the structure - "return the answer that occurs last in the
        input". What I wrote down then was that stipulation is a non-structural
        reason a choice is free, and that the five candidate axes had all been
        hunting inside the structure for something that was sitting outside it.

        What I did not ask is what a stipulated tie-break *costs*. On 685 it was
        one line: try `second` before `first`, and the convention is compiled
        into the control flow. Load-bearing, but free - the case analysis would
        have been written the same way either way, and no part of the
        correctness argument mentions the tie-break. So the working assumption
        going in was that a stipulation is always like that: a convention that
        the code has to respect somewhere and that the proof never sees.

        This is the problem where that fails, and it fails for a reason I did
        not have in advance.

        The tie-break here cannot sit beside the algorithm because the objective
        is not settled when a cell is first reached. So the key becomes the pair
        `(distance, instructions)` under the lexicographic product order and the
        stipulation is promoted into the objective itself. That much I expected.
        What I did not expect is that promoting it needs an argument, because
        Dijkstra's correctness wants the key to be monotone under extension - if
        `a < b` then `a + s < b + s` for every continuation `s` - and lex order
        on strings is *not*. Take `a = "l"`, `b = "lu"` and `s = "d"`: `a < b`
        but `"ld" > "lud"`. The order fails on exactly the pairs where one string
        is a proper prefix of the other.

        And those pairs cannot occur here, for a reason supplied by the other
        half of the key. Two instruction strings are only ever compared when
        their distances are equal and their endpoints are the same. If one were a
        proper prefix of the other, the longer one would be the shorter one plus
        a nonempty closed walk from that endpoint back to itself, and every roll
        that moves at all costs at least one cell, so the longer one has strictly
        greater distance. Equal distance rules the prefix case out.

        So the stipulated tie-break is usable as an optimisation key only
        because the thing it is tie-breaking forbids the case where it would
        misbehave. That is a genuinely different relationship from 685's, where
        the stipulation and the algorithm touched at one line and had nothing to
        say to each other. Here the two components of the key are not
        independent: the primary one is what licenses the secondary one.

        Which means "stipulated" and "free" are not the same property, and I had
        been treating them as one word. 685's tie-break was stipulated and free.
        This one is stipulated and owes a compatibility proof. The axis the log
        wanted all week - what makes a choice cost something - is not about where
        the choice comes from at all. It is about whether the choice has to be
        *carried through* a construction, and a tie-break carried through an
        optimisation has to commute with it.

        `O(R * C * log(R * C) * L)` with `L` the length of the winning
        instruction string, since the strings themselves are compared and copied
        rather than pointed at. Keeping parent pointers and reconstructing would
        drop the factor; it would also mean comparing two candidate paths by
        walking backwards from a shared endpoint, and the comparison is the part
        of this problem worth reading, so it stays in the key.
        """
        start, target = (ball[0], ball[1]), (hole[0], hole[1])
        settled: Set[Tuple[int, int]] = set()
        heap = [(0, "", start)]

        while heap:
            dist, path, cell = heapq.heappop(heap)
            if cell == target:
                # the first pop of the hole is optimal on both components at
                # once, which is the whole content of using the product order as
                # the key rather than filtering afterwards.
                return path
            if cell in settled:
                continue
            settled.add(cell)
            for letter, dr, dc in MOVES:
                nr, nc, moved = roll(maze, cell[0], cell[1], dr, dc, target)
                if moved == 0 or (nr, nc) in settled:
                    # `moved == 0` is a roll straight into a wall. it is not a
                    # move, and admitting it would let a path grow letters
                    # without spending distance - which is precisely the prefix
                    # case the monotonicity argument above rules out, so the
                    # guard is doing more than skipping a no-op.
                    continue
                heapq.heappush(heap, (dist + moved, path + letter, (nr, nc)))

        return "impossible"


if __name__ == "__main__":
    solution = Solution()

    maze_a = [
        [0, 0, 0, 0, 0],
        [1, 1, 0, 0, 1],
        [0, 0, 0, 0, 0],
        [0, 1, 0, 0, 1],
        [0, 1, 0, 0, 0],
    ]
    maze_b = [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 1, 0],
        [0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 1],
    ]

    # the first case is the one that matters: two instruction strings reach the
    # hole at distance 6 and the shorter of them is not the answer, so the
    # tie-break is doing visible work rather than breaking a symmetry nobody
    # would have noticed.
    cases = [
        (maze_a, [4, 3], [0, 1], "lul"),
        (maze_a, [4, 3], [3, 0], "impossible"),
        (maze_b, [0, 4], [3, 5], "dldr"),
    ]
    for maze, ball, hole, expected in cases:
        got = solution.findShortestWay(maze, ball, hole)
        optimal = all_optimal_paths(maze, ball, hole)
        print(
            f"ball={str(ball):<8} hole={str(hole):<8} -> {got:<11}"
            f" expected {expected:<11} {'ok' if got == expected else 'FAIL'}"
            f"   |optimal|={len(optimal)} {optimal}"
        )
        assert got == expected, (ball, hole, got, expected)
        if optimal:
            # the fast routine never builds this set, and the property it is
            # asserted against - least element of the tie - is the statement's
            # convention rather than anything the search evaluates.
            assert got == optimal[0], (got, optimal)
            assert len(got) >= min(len(p) for p in optimal), (
                "a lex-smallest optimal path can be longer than a shortest one, "
                "which is the case worth keeping"
            )
        else:
            assert got == "impossible", got
