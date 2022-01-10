from typing import List

class Solution:
    def simplifyPath(self, path: str) -> str:
        stack: List[str] = []
        for part in path.split("/"):
            if part == "" or part == ".":
                continue
            if part == "..":
                if stack:
                    stack.pop()
            else:
                stack.append(part)
        return "/" + "/".join(stack)
# follow up: revisit if profiling cares
