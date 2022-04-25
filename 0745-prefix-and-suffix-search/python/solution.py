from typing import List, Dict

class Trie:
    def __init__(self) -> None:
        self.children: Dict[str, "Trie"] = {}
        self.weight: int = -1

class WordFilter:
    def __init__(self, words: List[str]) -> None:
        self.root = Trie()
        for idx, w in enumerate(words):
            for s in range(len(w) + 1):
                key = w[s:] + "#" + w
                node = self.root
                for ch in key:
                    if ch not in node.children:
                        node.children[ch] = Trie()
                    node = node.children[ch]
                    node.weight = idx

    def f(self, pref: str, suff: str) -> int:
        node = self.root
        for ch in suff + "#" + pref:
            if ch not in node.children:
                return -1
            node = node.children[ch]
        return node.weight
# small style pass
