# singly linked list, sorted in non-decreasing order
# delete duplicates so each value appears once, return head


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def deleteDuplicates(self, head):
        # since the list is sorted, equal values are always adjacent
        # walk with a single pointer and skip over neighbours that match
        cur = head
        while cur and cur.next:
            if cur.val == cur.next.val:
                # bypass the duplicate node, keep cur in place to check the next pair
                cur.next = cur.next.next
            else:
                cur = cur.next
        return head


# small helper for local testing
def from_list(values):
    dummy = ListNode()
    tail = dummy
    for v in values:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next


def to_list(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out


if __name__ == "__main__":
    cases = [
        ([1, 1, 2], [1, 2]),
        ([1, 1, 2, 3, 3], [1, 2, 3]),
        ([], []),
        ([1], [1]),
        ([1, 1, 1, 1], [1]),
        ([-3, -3, -2, 0, 0, 0, 5], [-3, -2, 0, 5]),
    ]
    for nums, expected in cases:
        got = to_list(Solution().deleteDuplicates(from_list(nums)))
        assert got == expected, (nums, got, expected)
    print("ok")
