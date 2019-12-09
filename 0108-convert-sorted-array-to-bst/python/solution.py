class Solution:
    def sortedArrayToBST(self, nums):
        def build(l, r):
            if l > r:
                return None
            mid = (l + r) // 2
            node = TreeNode(nums[mid])
            node.left = build(l, mid - 1)
            node.right = build(mid + 1, r)
            return node
        return build(0, len(nums) - 1)
