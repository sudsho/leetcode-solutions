# binary tree zigzag level order traversal
# left-to-right on level 0, right-to-left on level 1, then flip again, ...
# bfs by level and reverse alternate levels before appending


from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def zigzagLevelOrder(self, root):
        if not root:
            return []

        out = []
        q = deque([root])
        # parity: 0 means left->right, 1 means right->left
        left_to_right = True

        while q:
            level_size = len(q)
            level = []
            for _ in range(level_size):
                node = q.popleft()
                level.append(node.val)
                if node.left:
                    q.append(node.left)
                if node.right:
                    q.append(node.right)
            if not left_to_right:
                level.reverse()
            out.append(level)
            left_to_right = not left_to_right

        return out


# tiny helper to build a tree from a leetcode-style list with None placeholders
def build(values):
    if not values:
        return None
    it = iter(values)
    root = TreeNode(next(it))
    q = deque([root])
    for v in it:
        parent = q[0]
        # left slot first then right; pop parent once both slots are filled
        if not hasattr(parent, "_left_set"):
            if v is not None:
                parent.left = TreeNode(v)
                q.append(parent.left)
            parent._left_set = True
        else:
            if v is not None:
                parent.right = TreeNode(v)
                q.append(parent.right)
            q.popleft()
    return root


if __name__ == "__main__":
    cases = [
        ([3, 9, 20, None, None, 15, 7], [[3], [20, 9], [15, 7]]),
        ([1], [[1]]),
        ([], []),
        ([1, 2, 3, 4, None, None, 5], [[1], [3, 2], [4, 5]]),
    ]
    for values, expected in cases:
        got = Solution().zigzagLevelOrder(build(values))
        assert got == expected, (values, got, expected)
    print("ok")
