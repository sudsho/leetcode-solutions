from typing import Optional
from collections import deque

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def replaceValueInTree(self, root: Optional['TreeNode']) -> Optional['TreeNode']:
        if root is None:
            return None
        root.val = 0
        q: deque['TreeNode'] = deque([root])
        while q:
            sz = len(q)
            level_sum = 0
            row = []
            for _ in range(sz):
                u = q.popleft()
                level_sum += (u.left.val if u.left else 0) + (u.right.val if u.right else 0)
                row.append(u)
            for u in row:
                sib = (u.left.val if u.left else 0) + (u.right.val if u.right else 0)
                if u.left:
                    u.left.val = level_sum - sib
                    q.append(u.left)
                if u.right:
                    u.right.val = level_sum - sib
                    q.append(u.right)
        return root
