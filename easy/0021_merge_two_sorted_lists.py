# Merge two sorted linked lists into one sorted linked list.
# Use a dummy head node and iteratively compare nodes from each list,
# appending the smaller node until one list is exhausted.

from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode(0)
        current = dummy

        while list1 and list2:
            if list1.val <= list2.val:
                current.next = list1
                list1 = list1.next
            else:
                current.next = list2
                list2 = list2.next
            current = current.next

        # Attach the remaining nodes
        current.next = list1 if list1 else list2

        return dummy.next


# Time Complexity: O(m + n) where m and n are lengths of the two lists
# Space Complexity: O(1) — only pointer manipulation, no extra allocations


def list_to_linked(vals):
    dummy = ListNode(0)
    cur = dummy
    for v in vals:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def linked_to_list(node):
    result = []
    while node:
        result.append(node.val)
        node = node.next
    return result


if __name__ == "__main__":
    sol = Solution()

    # Test 1: [1,2,4] + [1,3,4] -> [1,1,2,3,4,4]
    l1 = list_to_linked([1, 2, 4])
    l2 = list_to_linked([1, 3, 4])
    print(linked_to_list(sol.mergeTwoLists(l1, l2)))  # [1, 1, 2, 3, 4, 4]

    # Test 2: [] + [] -> []
    print(linked_to_list(sol.mergeTwoLists(None, None)))  # []

    # Test 3: [] + [0] -> [0]
    l2 = list_to_linked([0])
    print(linked_to_list(sol.mergeTwoLists(None, l2)))  # [0]
