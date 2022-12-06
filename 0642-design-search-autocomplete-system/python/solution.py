from typing import List, Dict

class Trie:
    def __init__(self) -> None:
        self.children: Dict[str, "Trie"] = {}
        self.counts: Dict[str, int] = {}

class AutocompleteSystem:
    def __init__(self, sentences: List[str], times: List[int]) -> None:
        self.root = Trie()
        for s, t in zip(sentences, times):
            self._insert(s, t)
        self.curr = ""
        self.node = self.root

    def _insert(self, s: str, count: int) -> None:
        node = self.root
        for ch in s:
            if ch not in node.children:
                node.children[ch] = Trie()
            node = node.children[ch]
            node.counts[s] = node.counts.get(s, 0) + count

    def input(self, c: str) -> List[str]:
        if c == "#":
            self._insert(self.curr, 1)
            self.curr = ""
            self.node = self.root
            return []
        self.curr += c
        if self.node and c in self.node.children:
            self.node = self.node.children[c]
        else:
            self.node = None
        if not self.node:
            return []
        items = list(self.node.counts.items())
        items.sort(key=lambda x: (-x[1], x[0]))
        return [s for s, _ in items[:3]]
