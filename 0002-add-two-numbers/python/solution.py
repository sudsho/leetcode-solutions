# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def addTwoNumbers(self, l1, l2):
        # digits are stored in reverse, so traversal order already matches
        # the order we'd add by hand. carry handles the overflow each step.
        dummy = ListNode()
        tail = dummy
        carry = 0
        while l1 or l2 or carry:
            a = l1.val if l1 else 0
            b = l2.val if l2 else 0
            s = a + b + carry
            carry, digit = divmod(s, 10)
            tail.next = ListNode(digit)
            tail = tail.next
            if l1:
                l1 = l1.next
            if l2:
                l2 = l2.next
        return dummy.next
