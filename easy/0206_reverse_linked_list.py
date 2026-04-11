# Reverse a singly linked list.
# Given the head of a linked list, reverse it and return the new head.
# Classic iterative approach using three pointers (prev, curr, next).

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def reverseList(self, head: ListNode) -> ListNode:
        prev = None
        curr = head
        while curr:
            next_node = curr.next
            curr.next = prev
            prev = curr
            curr = next_node
        return prev


# Time:  O(n) — single pass through all n nodes
# Space: O(1) — only three pointers, no extra data structures

if __name__ == "__main__":
    def build(vals):
        dummy = ListNode(0)
        cur = dummy
        for v in vals:
            cur.next = ListNode(v)
            cur = cur.next
        return dummy.next

    def to_list(head):
        result = []
        while head:
            result.append(head.val)
            head = head.next
        return result

    s = Solution()

    # Test 1: [1,2,3,4,5] → [5,4,3,2,1]
    print(to_list(s.reverseList(build([1, 2, 3, 4, 5]))))  # [5, 4, 3, 2, 1]

    # Test 2: [1,2] → [2,1]
    print(to_list(s.reverseList(build([1, 2]))))            # [2, 1]

    # Test 3: [] → []
    print(to_list(s.reverseList(None)))                     # []
