# alt: paired hash map of (prefix, suffix) -> idx
from typing import List, Dict

class WordFilter:
    def __init__(self, words: List[str]) -> None:
        self.lookup: Dict[tuple, int] = {}
        for idx, w in enumerate(words):
            for i in range(len(w) + 1):
                for j in range(len(w) + 1):
                    self.lookup[(w[:i], w[j:])] = idx

    def f(self, pref: str, suff: str) -> int:
        return self.lookup.get((pref, suff), -1)
