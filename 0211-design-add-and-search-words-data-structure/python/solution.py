class TrieNode:
    __slots__ = ("children", "end")

    def __init__(self):
        self.children = {}
        self.end = False


class WordDictionary:
    """Prefix tree that supports '.' as a single-character wildcard on search.

    addWord walks/creates a path down the trie. search does the same, but at a
    '.' it branches into every child, so it's a small DFS rather than a plain
    walk. Only wildcards fan out, so most searches stay close to O(len).
    """

    def __init__(self):
        self.root = TrieNode()

    def addWord(self, word: str) -> None:
        node = self.root
        for ch in word:
            node = node.children.setdefault(ch, TrieNode())
        node.end = True

    def search(self, word: str) -> bool:
        def dfs(node, i: int) -> bool:
            if i == len(word):
                return node.end
            ch = word[i]
            if ch == ".":
                return any(dfs(child, i + 1) for child in node.children.values())
            nxt = node.children.get(ch)
            return dfs(nxt, i + 1) if nxt else False

        return dfs(self.root, 0)
