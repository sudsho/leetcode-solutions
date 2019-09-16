# alt approach: hash-set approach. extra space but simpler logic

class Solution:
    def hasCycle(self, head):
        # set of seen nodes - O(n) extra space
        seen = set()
        cur = head
        while cur:
            if cur in seen:
                return True
            seen.add(cur)
            cur = cur.next
        return False
