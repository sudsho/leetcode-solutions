class Solution:
    def isIsomorphic(self, s, t):
        """Two strings are isomorphic if there is a consistent one-to-one
        character mapping from s to t. Track both directions so the mapping
        stays a bijection (no two source chars map to the same target)."""
        if len(s) != len(t):
            return False
        forward = {}
        backward = {}
        for a, b in zip(s, t):
            if a in forward and forward[a] != b:
                return False
            if b in backward and backward[b] != a:
                return False
            forward[a] = b
            backward[b] = a
        return True
