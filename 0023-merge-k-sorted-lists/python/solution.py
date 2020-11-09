import heapq

class Solution:
    def mergeKLists(self, lists):
        # heapq compares tuples; (val, idx, node) - idx breaks ties for same val
        h = []
        for i, node in enumerate(lists):
            if node:
                heapq.heappush(h, (node.val, i, node))
        dummy = ListNode(0)
        tail = dummy
        while h:
            val, i, node = heapq.heappop(h)
            tail.next = node
            tail = tail.next
            if node.next:
                heapq.heappush(h, (node.next.val, i, node.next))
        return dummy.next
