from typing import List

class Solution:
    def minSwapsCouples(self, row: List[int]) -> int:
        # Greedy with index map
        pos = {v: i for i, v in enumerate(row)}
        swaps = 0
        for i in range(0, len(row), 2):
            partner = row[i] ^ 1
            if row[i + 1] == partner:
                continue
            j = pos[partner]
            row[i + 1], row[j] = row[j], row[i + 1]
            pos[row[j]] = j
            pos[row[i + 1]] = i + 1
            swaps += 1
        return swaps
