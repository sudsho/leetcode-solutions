from typing import List
from bisect import bisect_left

class Solution:
    def suggestedProducts(self, products: List[str], searchWord: str) -> List[List[str]]:
        products.sort()
        out: List[List[str]] = []
        prefix = ""
        i = 0
        for c in searchWord:
            prefix += c
            i = bisect_left(products, prefix, i)
            out.append([w for w in products[i:i + 3] if w.startswith(prefix)])
        return out
