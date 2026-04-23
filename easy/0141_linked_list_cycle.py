# Detect if a linked list has a cycle using Floyd's slow/fast pointer algorithm.
# If the two pointers ever point to the same node, a cycle exists.

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def hasCycle(self, head: ListNode) -> bool:
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow is fast:
                return True
        return False

# Time: O(n) | Space: O(1)

if __name__ == "__main__":
    # Build list 3 -> 2 -> 0 -> -4 -> (back to node 2)
    n3, n2, n0, n4 = ListNode(3), ListNode(2), ListNode(0), ListNode(-4)
    n3.next, n2.next, n0.next, n4.next = n2, n0, n4, n2
    assert Solution().hasCycle(n3) == True

    # No cycle: 1 -> 2
    a, b = ListNode(1), ListNode(2)
    a.next = b
    assert Solution().hasCycle(a) == False

    # Single node, no cycle
    assert Solution().hasCycle(ListNode(1)) == False

    print("all tests passed")
