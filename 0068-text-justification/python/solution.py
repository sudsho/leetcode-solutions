from typing import List

class Solution:
    def fullJustify(self, words: List[str], maxWidth: int) -> List[str]:
        result: List[str] = []
        i, n = 0, len(words)
        while i < n:
            j = i
            line_len = len(words[j])
            j += 1
            while j < n and line_len + 1 + len(words[j]) <= maxWidth:
                line_len += 1 + len(words[j])
                j += 1
            gap_count = j - i - 1
            slack = maxWidth - sum(len(words[k]) for k in range(i, j))
            if j == n or gap_count == 0:
                line = " ".join(words[i:j])
                line += " " * (maxWidth - len(line))
            else:
                base, extra = divmod(slack, gap_count)
                parts = []
                for idx in range(i, j - 1):
                    parts.append(words[idx])
                    parts.append(" " * (base + (1 if idx - i < extra else 0)))
                parts.append(words[j - 1])
                line = "".join(parts)
            result.append(line)
            i = j
        return result
