# Given a binary tree, return its level-order traversal as a list of lists.
# Each inner list contains the values of nodes at that depth level.
# Uses BFS with a queue to process nodes level by level.

from collections import deque
from typing import Optional, List


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if not root:
            return []

        result = []
        queue = deque([root])

        while queue:
            level_size = len(queue)
            level = []

            for _ in range(level_size):
                node = queue.popleft()
                level.append(node.val)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

            result.append(level)

        return result

# Time:  O(n) - visit every node once
# Space: O(n) - queue holds at most n/2 nodes at the widest level


if __name__ == "__main__":
    sol = Solution()

    # Test 1: [3,9,20,null,null,15,7] → [[3],[9,20],[15,7]]
    root = TreeNode(3)
    root.left = TreeNode(9)
    root.right = TreeNode(20)
    root.right.left = TreeNode(15)
    root.right.right = TreeNode(7)
    print(sol.levelOrder(root))  # [[3], [9, 20], [15, 7]]

    # Test 2: single node → [[1]]
    print(sol.levelOrder(TreeNode(1)))  # [[1]]

    # Test 3: empty tree → []
    print(sol.levelOrder(None))  # []
