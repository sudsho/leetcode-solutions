# regex-backed quick check
import re

class Solution:
    _PATTERN = re.compile(r"^[+-]?(\d+\.?\d*|\.\d+)([eE][+-]?\d+)?$")

    def isNumber(self, s: str) -> bool:
        return bool(self._PATTERN.match(s.strip()))
