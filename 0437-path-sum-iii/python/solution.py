from collections import defaultdict

class Solution:
    def pathSum(self, root, targetSum):
        prefix = defaultdict(int)
        prefix[0] = 1
        self.count = 0

        def dfs(node, cur):
            if not node:
                return
            cur += node.val
            self.count += prefix[cur - targetSum]
            prefix[cur] += 1
            dfs(node.left, cur)
            dfs(node.right, cur)
            prefix[cur] -= 1

        dfs(root, 0)
        return self.count
# typing fix
