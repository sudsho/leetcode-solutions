from typing import List

class Solution:
    def doesValidArrayExist(self, derived: List[int]) -> bool:
        return sum(derived) % 2 == 0

# revisit: minor renames and one early exit added
