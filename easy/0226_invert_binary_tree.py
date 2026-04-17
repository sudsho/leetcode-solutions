# Given the root of a binary tree, invert it (mirror it) and return its root.
# Swapping left and right children recursively at each node produces the mirror image.
# Classic example of a simple but elegant recursive tree problem.

from collections import deque
from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        if root is None:
            return None
        root.left, root.right = self.invertTree(root.right), self.invertTree(root.left)
        return root


# Time: O(n) — visit every node once
# Space: O(h) — recursion stack, h = height of tree (O(log n) balanced, O(n) worst)


def build_tree(vals):
    if not vals:
        return None
    root = TreeNode(vals[0])
    queue = deque([root])
    i = 1
    while queue and i < len(vals):
        node = queue.popleft()
        if i < len(vals) and vals[i] is not None:
            node.left = TreeNode(vals[i])
            queue.append(node.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            node.right = TreeNode(vals[i])
            queue.append(node.right)
        i += 1
    return root


def tree_to_list(root):
    if not root:
        return []
    result, queue = [], deque([root])
    while queue:
        node = queue.popleft()
        if node:
            result.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
        else:
            result.append(None)
    while result and result[-1] is None:
        result.pop()
    return result


if __name__ == "__main__":
    sol = Solution()

    # Test 1: [4,2,7,1,3,6,9] -> [4,7,2,9,6,3,1]
    root = build_tree([4, 2, 7, 1, 3, 6, 9])
    print(tree_to_list(sol.invertTree(root)))  # [4, 7, 2, 9, 6, 3, 1]

    # Test 2: [2,1,3] -> [2,3,1]
    root = build_tree([2, 1, 3])
    print(tree_to_list(sol.invertTree(root)))  # [2, 3, 1]

    # Test 3: [] -> []
    root = build_tree([])
    print(tree_to_list(sol.invertTree(root)))  # []
