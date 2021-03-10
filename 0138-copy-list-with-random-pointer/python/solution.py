class Node:
    def __init__(self, x: int, next: "Node" = None, random: "Node" = None):
        self.val = x
        self.next = next
        self.random = random


class Solution:
    def copyRandomList(self, head):
        if not head:
            return None
        m = {}
        cur = head
        while cur:
            m[cur] = Node(cur.val)
            cur = cur.next
        cur = head
        while cur:
            m[cur].next = m.get(cur.next)
            m[cur].random = m.get(cur.random)
            cur = cur.next
        return m[head]
