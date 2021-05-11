# prefix sum variant O(n)
from collections import defaultdict

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def pathSum(self, root, target: int) -> int:
        prefix = defaultdict(int)
        prefix[0] = 1
        ans = 0

        def dfs(node, running: int) -> None:
            nonlocal ans
            if not node:
                return
            running += node.val
            ans += prefix[running - target]
            prefix[running] += 1
            dfs(node.left, running)
            dfs(node.right, running)
            prefix[running] -= 1

        dfs(root, 0)
        return ans
