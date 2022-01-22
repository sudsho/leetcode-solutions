# regex split + filter, more pythonic
import re

class Solution:
    def simplifyPath(self, path: str) -> str:
        stack = []
        for part in re.split(r"/+", path):
            if part in ("", "."):
                continue
            if part == "..":
                if stack:
                    stack.pop()
            else:
                stack.append(part)
        return "/" + "/".join(stack)
# follow up: revisit if profiling cares
