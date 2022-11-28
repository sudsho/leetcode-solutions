# regex split, lstrip zero-padded segments
import re

class Solution:
    def compareVersion(self, version1: str, version2: str) -> int:
        a = [int(x) for x in re.split(r"\.", version1)]
        b = [int(x) for x in re.split(r"\.", version2)]
        for i in range(max(len(a), len(b))):
            x = a[i] if i < len(a) else 0
            y = b[i] if i < len(b) else 0
            if x != y:
                return -1 if x < y else 1
        return 0
