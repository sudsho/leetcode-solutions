class Solution:
    def cloneGraph(self, node):
        if not node:
            return None
        memo = {}

        def dfs(n):
            if n in memo:
                return memo[n]
            copy = Node(n.val)
            memo[n] = copy
            for nb in n.neighbors:
                copy.neighbors.append(dfs(nb))
            return copy

        return dfs(node)
