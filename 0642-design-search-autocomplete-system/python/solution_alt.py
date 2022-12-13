# BFS variant: enumerate matches per char without modifying root
from typing import List, Dict
from collections import defaultdict

class AutocompleteSystem:
    def __init__(self, sentences: List[str], times: List[int]) -> None:
        self.counts: Dict[str, int] = defaultdict(int)
        for s, t in zip(sentences, times):
            self.counts[s] += t
        self.curr = ""

    def input(self, c: str) -> List[str]:
        if c == "#":
            self.counts[self.curr] += 1
            self.curr = ""
            return []
        self.curr += c
        matches = [s for s in self.counts if s.startswith(self.curr)]
        matches.sort(key=lambda s: (-self.counts[s], s))
        return matches[:3]
