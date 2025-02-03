# revisited
class Solution:
    def isPalindrome(self, head):
        # easy version - copy values to a list
        vals = []
        cur = head
        while cur:
            vals.append(cur.val)
            cur = cur.next
        return vals == vals[::-1]

# revisit: minor renames and one early exit added
