from typing import List

class Solution:
    def shortestSuperstring(self, words: List[str]) -> str:
        # Greedy merge by max overlap. Heuristic; not optimal but commonly tried first.
        words = list(set(words))

        def overlap(a: str, b: str) -> int:
            lim = min(len(a), len(b))
            for k in range(lim, 0, -1):
                if a[-k:] == b[:k]:
                    return k
            return 0

        while len(words) > 1:
            best_i = best_j = -1
            best_ov = -1
            best_merged = ''
            for i in range(len(words)):
                for j in range(len(words)):
                    if i == j:
                        continue
                    ov = overlap(words[i], words[j])
                    if ov > best_ov:
                        best_ov = ov
                        best_i, best_j = i, j
                        best_merged = words[i] + words[j][ov:]
            words = [w for k, w in enumerate(words) if k != best_i and k != best_j]
            words.append(best_merged)
        return words[0] if words else ''
