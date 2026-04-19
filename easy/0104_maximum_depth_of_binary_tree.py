# Given the root of a binary tree, return its maximum depth.
# Maximum depth = number of nodes along the longest path from root to a leaf.
# Recursive DFS: depth at each node = 1 + max(left_depth, right_depth)

from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
        return 1 + max(self.maxDepth(root.left), self.maxDepth(root.right))


# Time: O(n) - every node visited once
# Space: O(h) - recursion stack, O(log n) average / O(n) worst (skewed tree)


if __name__ == "__main__":
    # Test 1: [3, 9, 20, null, null, 15, 7] -> expected 3
    root = TreeNode(3)
    root.left = TreeNode(9)
    root.right = TreeNode(20)
    root.right.left = TreeNode(15)
    root.right.right = TreeNode(7)
    print(Solution().maxDepth(root))   # 3

    # Test 2: [1, null, 2] -> expected 2
    root2 = TreeNode(1)
    root2.right = TreeNode(2)
    print(Solution().maxDepth(root2))  # 2

    # Test 3: empty tree -> expected 0
    print(Solution().maxDepth(None))   # 0
