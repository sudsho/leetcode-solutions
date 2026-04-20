# Given a binary tree, find the maximum path sum where a path is any sequence
# of nodes connected by parent-child edges. The path can start and end anywhere
# in the tree and must contain at least one node.

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def maxPathSum(self, root: TreeNode) -> int:
        self.max_sum = float('-inf')

        def dfs(node):
            if not node:
                return 0

            # only take positive contributions from children
            left_gain = max(dfs(node.left), 0)
            right_gain = max(dfs(node.right), 0)

            # path through this node connecting both subtrees
            path_through = node.val + left_gain + right_gain
            self.max_sum = max(self.max_sum, path_through)

            # return max gain if we extend upward (can only pick one branch)
            return node.val + max(left_gain, right_gain)

        dfs(root)
        return self.max_sum


if __name__ == "__main__":
    sol = Solution()

    # Test 1: [1,2,3] -> expected 6
    root1 = TreeNode(1, TreeNode(2), TreeNode(3))
    print(sol.maxPathSum(root1))  # 6

    # Test 2: [-10,9,20,null,null,15,7] -> expected 42
    root2 = TreeNode(-10)
    root2.left = TreeNode(9)
    root2.right = TreeNode(20, TreeNode(15), TreeNode(7))
    print(sol.maxPathSum(root2))  # 42

    # Test 3: single negative node [-3] -> expected -3
    root3 = TreeNode(-3)
    print(sol.maxPathSum(root3))  # -3

# Time:  O(n) - each node visited once via DFS
# Space: O(h) - call stack depth equals tree height h (O(log n) balanced, O(n) skewed)
