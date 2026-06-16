from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def levelOrderBottom(self, root):
        """Level-order values, but ordered from the deepest level up to the root.

        This is plain BFS by levels - snapshot the queue size at the start of
        each level so the inner loop drains exactly that many nodes - and then
        the bottom-up requirement is just the top-down result reversed. Building
        top-down and reversing once at the end is O(L) for L levels and keeps the
        traversal itself completely ordinary; the alternative of inserting each
        level at the front of the result list would cost O(L) per insert.
        """
        levels = []
        if root is None:
            return levels
        queue = deque([root])
        while queue:
            level = []
            for _ in range(len(queue)):  # only the nodes already on this level
                node = queue.popleft()
                level.append(node.val)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            levels.append(level)
        levels.reverse()  # top-down -> bottom-up in one pass
        return levels


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
    assert s.levelOrderBottom(_build([3, 9, 20, None, None, 15, 7])) == [
        [15, 7],
        [9, 20],
        [3],
    ]
    assert s.levelOrderBottom(_build([1])) == [[1]]
    assert s.levelOrderBottom(None) == []
    print("all good")
