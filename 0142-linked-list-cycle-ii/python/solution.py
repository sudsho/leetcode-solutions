class Solution:
    def detectCycle(self, head):
        if not head:
            return None
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow == fast:
                # find entry
                p = head
                while p != slow:
                    p = p.next
                    slow = slow.next
                return p
        return None
