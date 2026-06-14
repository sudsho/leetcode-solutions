# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def rob(self, root):
        """Max money robbable without alarming two directly-linked houses.

        Tree DP: for each node return a pair (rob_this, skip_this).
        - rob_this  = node.val + skip(left) + skip(right)   (children must be skipped)
        - skip_this = max(rob, skip)(left) + max(rob, skip)(right)  (children free)
        The answer is the better of the two options at the root.
        """

        def walk(node):
            if node is None:
                return 0, 0  # (rob, skip) for an empty subtree
            l_rob, l_skip = walk(node.left)
            r_rob, r_skip = walk(node.right)
            rob = node.val + l_skip + r_skip
            skip = max(l_rob, l_skip) + max(r_rob, r_skip)
            return rob, skip

        return max(walk(root))
