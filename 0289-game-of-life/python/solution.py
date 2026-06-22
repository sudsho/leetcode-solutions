class Solution:
    def gameOfLife(self, board):
        """Advance Conway's Game of Life one generation, in place.

        The catch with an in-place update is that every cell's next state
        depends on its neighbours' *current* states, so we cannot overwrite a
        cell with a plain 0/1 or later neighbours would read the new value
        instead of the old one. The trick is to encode both states in one cell
        using the second bit while leaving the low bit as the original value:

            bit 0 -> current (live/dead) state
            bit 1 -> next state

        While scanning we only ever read `cell & 1` (the original), and we set
        bit 1 when a cell should be alive next turn. A final pass shifts every
        cell right by one so the next state becomes the only state. This keeps
        the whole thing O(1) extra space.
        """
        if not board or not board[0]:
            return

        rows, cols = len(board), len(board[0])

        for r in range(rows):
            for c in range(cols):
                live = self._live_neighbors(board, r, c, rows, cols)
                # A live cell survives with 2 or 3 neighbours; a dead cell is
                # born with exactly 3. Both rules collapse to writing bit 1.
                if board[r][c] & 1:
                    if live == 2 or live == 3:
                        board[r][c] |= 2
                else:
                    if live == 3:
                        board[r][c] |= 2

        for r in range(rows):
            for c in range(cols):
                board[r][c] >>= 1  # promote next state to the only state

    def _live_neighbors(self, board, r, c, rows, cols):
        """Count currently-live cells in the 8-neighbourhood of (r, c).

        Reads the low bit only, so it is unaffected by next-state marks already
        written into bit 1 of earlier cells in the same sweep.
        """
        count = 0
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    count += board[nr][nc] & 1
        return count


if __name__ == "__main__":
    # LeetCode example 1: blinker-like configuration.
    grid = [[0, 1, 0],
            [0, 0, 1],
            [1, 1, 1],
            [0, 0, 0]]
    Solution().gameOfLife(grid)
    expected = [[0, 0, 0],
                [1, 0, 1],
                [0, 1, 1],
                [0, 1, 0]]
    assert grid == expected, grid

    # Edge case: a board with no live cells must stay all-dead.
    dead = [[0, 0], [0, 0]]
    Solution().gameOfLife(dead)
    assert dead == [[0, 0], [0, 0]], dead

    # Edge case: a lone live cell has zero neighbours and dies of underpopulation.
    lonely = [[1]]
    Solution().gameOfLife(lonely)
    assert lonely == [[0]], lonely

    print("ok:", grid)
