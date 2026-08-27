from typing import List, Tuple

Shape = Tuple[Tuple[int, int], ...]

# the eight elements of D4 acting on the integer plane, written as the maps they
# induce on a cell. rotations are (x,y) -> (y,-x) and its powers, reflections are
# those composed with (x,y) -> (x,-y). listing them explicitly is clearer here
# than generating the group, and eight is not worth a loop over generators.
TRANSFORMS = (
    lambda r, c: (r, c),
    lambda r, c: (r, -c),
    lambda r, c: (-r, c),
    lambda r, c: (-r, -c),
    lambda r, c: (c, r),
    lambda r, c: (c, -r),
    lambda r, c: (-c, r),
    lambda r, c: (-c, -r),
)


class Solution:
    def numDistinctIslands2(self, grid: List[List[int]]) -> int:
        if not grid or not grid[0]:
            return 0
        rows, cols = len(grid), len(grid[0])
        seen = [[False] * cols for _ in range(rows)]

        shapes = set()
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == 1 and not seen[r][c]:
                    shapes.add(canonical(flood(grid, seen, r, c)))
        return len(shapes)


def flood(grid: List[List[int]], seen: List[List[bool]], sr: int, sc: int) -> List[Tuple[int, int]]:
    """Collect one 4-connected component of 1s, marking it visited."""
    rows, cols = len(grid), len(grid[0])
    stack = [(sr, sc)]
    seen[sr][sc] = True
    cells = []
    while stack:
        r, c = stack.pop()
        cells.append((r, c))
        for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1 and not seen[nr][nc]:
                seen[nr][nc] = True
                stack.append((nr, nc))
    return cells


def canonical(cells: List[Tuple[int, int]]) -> Shape:
    """A representative of the island's orbit under translations and D4.

    Two islands are the same shape iff their cell sets differ by an element of
    Z^2 x| D4, so counting shapes is counting orbits, and the orbit set is the
    quotient of the set of islands by that group. The quotient is determined -
    there is no choice in it - but a hash set needs an element of each orbit, not
    the orbit, so what this returns is a section of the quotient map. Sections
    are chosen. Any function constant on orbits and injective across them works
    just as well; this one is only the cheapest to write down.

    The two halves of the group are handled by different mechanisms, and they
    have to be, because they are differently shaped:

    - the translation subgroup acts freely and its orbits are infinite, so no
      enumeration is available and the representative has to be a normal form.
      it is one: translate so the minimum cell is the origin. that is well
      defined because Z^2 is ordered and the order is translation-equivariant.
    - D4 is finite (order 8) and does *not* act freely - a symmetric island is
      fixed by some of it - so there is no fundamental domain to normalize into.
      but the orbit is small enough to write out in full, and a min over it is
      then well defined for the trivial reason that a finite set of tuples has
      a least element. that is a choice with nothing distinguishing it: no order
      on the plane is D4-equivariant, so `min` here is a tie-break and not a
      structure.

    So: enumerate the 8 images, normalize each by translation, take the least.
    O(8 * s log s) for an island of s cells.
    """
    best = None
    for t in TRANSFORMS:
        moved = sorted(t(r, c) for r, c in cells)
        # normalize the translation: sorting puts the least cell first, and
        # subtracting it is exactly the fundamental-domain choice above. the
        # list stays sorted under a uniform shift, so no re-sort.
        br, bc = moved[0]
        shape = tuple((r - br, c - bc) for r, c in moved)
        # min over the 8, not over the distinct ones. an island with a
        # nontrivial stabilizer produces the same shape more than once here and
        # deduplicating first would change nothing, since min reads only the
        # support of the multiset.
        if best is None or shape < best:
            best = shape
    return best
