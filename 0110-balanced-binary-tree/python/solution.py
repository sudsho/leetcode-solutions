class Solution:
    def isBalanced(self, root):
        # bottom up - return height, or -1 to signal "already unbalanced"
        def check(node):
            if node is None:
                return 0
            l = check(node.left)
            if l == -1:
                return -1
            r = check(node.right)
            if r == -1:
                return -1
            if abs(l - r) > 1:
                return -1
            return 1 + max(l, r)

        return check(root) != -1
