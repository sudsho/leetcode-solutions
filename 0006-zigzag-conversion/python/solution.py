class Solution:
    def convert(self, s, numRows):
        # one row or taller than the string => already in the right order
        if numRows == 1 or numRows >= len(s):
            return s
        rows = [[] for _ in range(numRows)]
        r = 0
        step = 1
        for ch in s:
            rows[r].append(ch)
            if r == 0:
                step = 1
            elif r == numRows - 1:
                step = -1
            r += step
        return ''.join(''.join(row) for row in rows)
