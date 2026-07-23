# recursive variant of the iterative search in solution.py - same O(h) walk

class Solution:
    def searchBST(self, root, val):
        if root is None or root.val == val:
            return root
        if val < root.val:
            return self.searchBST(root.left, val)
        return self.searchBST(root.right, val)
