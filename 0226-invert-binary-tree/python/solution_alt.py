# alt approach: iterative BFS version of invertTree

class Solution:
    def invertTree(self, root):
        # iterative bfs version
        if not root:
            return None
        q = [root]
        while q:
            node = q.pop(0)
            node.left, node.right = node.right, node.left
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
        return root
