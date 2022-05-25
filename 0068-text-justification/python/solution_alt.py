# slightly more compact gap distribution
from typing import List

class Solution:
    def fullJustify(self, words: List[str], maxWidth: int) -> List[str]:
        out: List[str] = []
        line: List[str] = []
        line_len = 0
        for w in words:
            if line_len + len(w) + len(line) > maxWidth:
                # flush
                spaces = maxWidth - line_len
                if len(line) == 1:
                    out.append(line[0] + " " * spaces)
                else:
                    base, extra = divmod(spaces, len(line) - 1)
                    parts = []
                    for i, word in enumerate(line[:-1]):
                        parts.append(word)
                        parts.append(" " * (base + (1 if i < extra else 0)))
                    parts.append(line[-1])
                    out.append("".join(parts))
                line = []
                line_len = 0
            line.append(w)
            line_len += len(w)
        if line:
            tail = " ".join(line)
            out.append(tail + " " * (maxWidth - len(tail)))
        return out
