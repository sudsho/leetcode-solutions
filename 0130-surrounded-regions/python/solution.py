class Solution:
    def solve(self, board):
        if not board or not board[0]:
            return

        rows, cols = len(board), len(board[0])

        def mark(r, c):
            stack = [(r, c)]
            while stack:
                i, j = stack.pop()
                if i < 0 or i >= rows or j < 0 or j >= cols:
                    continue
                if board[i][j] != "O":
                    continue
                board[i][j] = "#"
                stack.append((i + 1, j))
                stack.append((i - 1, j))
                stack.append((i, j + 1))
                stack.append((i, j - 1))

        for r in range(rows):
            mark(r, 0)
            mark(r, cols - 1)
        for c in range(cols):
            mark(0, c)
            mark(rows - 1, c)

        for r in range(rows):
            for c in range(cols):
                if board[r][c] == "O":
                    board[r][c] = "X"
                elif board[r][c] == "#":
                    board[r][c] = "O"
