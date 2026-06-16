from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def minDepth(self, root):
        """Depth of the shallowest leaf, counting nodes from the root.

        The subtle part is the definition of "leaf": a node with exactly one
        child is NOT a leaf, so a naive `1 + min(left, right)` is wrong - it
        would return 1 for a root whose only child hangs off one side, cutting
        the path short at a missing subtree. BFS sidesteps the whole issue:
        scan level by level and return the depth of the first node we meet that
        has no children at all. Because BFS reaches nodes in nondecreasing depth
        order, that first leaf is guaranteed to be the shallowest one.
        """
        if root is None:
            return 0
        queue = deque([(root, 1)])
        while queue:
            node, depth = queue.popleft()
            if node.left is None and node.right is None:
                return depth  # first leaf in BFS order is the shallowest
            if node.left:
                queue.append((node.left, depth + 1))
            if node.right:
                queue.append((node.right, depth + 1))
        return 0  # unreachable: a non-empty tree always has a leaf


def _build(values):
    """Build a tree from a level-order list with None for missing children."""
    if not values:
        return None
    it = iter(values)
    root = TreeNode(next(it))
    queue = deque([root])
    while queue:
        node = queue.popleft()
        for side in ("left", "right"):
            try:
                v = next(it)
            except StopIteration:
                return root
            if v is not None:
                child = TreeNode(v)
                setattr(node, side, child)
                queue.append(child)
    return root


if __name__ == "__main__":
    s = Solution()
    assert s.minDepth(_build([3, 9, 20, None, None, 15, 7])) == 2
    assert s.minDepth(_build([2, None, 3, None, 4, None, 5, None, 6])) == 5
    assert s.minDepth(None) == 0
    assert s.minDepth(_build([1])) == 1
    print("all good")
