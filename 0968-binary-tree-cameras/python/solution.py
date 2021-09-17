class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def minCameraCover(self, root) -> int:
        # 0 = no camera + not covered, 1 = camera here, 2 = covered no camera
        self.cnt = 0

        def dfs(node) -> int:
            if not node:
                return 2
            l = dfs(node.left)
            r = dfs(node.right)
            if l == 0 or r == 0:
                self.cnt += 1
                return 1
            if l == 1 or r == 1:
                return 2
            return 0

        if dfs(root) == 0:
            self.cnt += 1
        return self.cnt
