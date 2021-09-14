# style tweak
class Codec:
    def serialize(self, root):
        out = []
        def go(node):
            if not node:
                out.append("#")
                return
            out.append(str(node.val))
            go(node.left)
            go(node.right)
        go(root)
        return ",".join(out)

    def deserialize(self, data):
        tokens = iter(data.split(","))

        def build():
            t = next(tokens)
            if t == "#":
                return None
            node = TreeNode(int(t))
            node.left = build()
            node.right = build()
            return node

        return build()
# typing fix
