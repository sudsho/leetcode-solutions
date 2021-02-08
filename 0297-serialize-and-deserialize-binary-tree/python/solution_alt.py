# preorder with sentinels variant
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Codec:
    def serialize(self, root) -> str:
        out = []

        def dfs(n) -> None:
            if not n:
                out.append("#")
                return
            out.append(str(n.val))
            dfs(n.left)
            dfs(n.right)

        dfs(root)
        return ",".join(out)

    def deserialize(self, data: str):
        it = iter(data.split(","))

        def build():
            v = next(it)
            if v == "#":
                return None
            n = TreeNode(int(v))
            n.left = build()
            n.right = build()
            return n

        return build()
