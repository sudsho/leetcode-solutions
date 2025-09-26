from typing import List
from collections import Counter

class Encrypter:
    def __init__(self, keys: List[str], values: List[str], dictionary: List[str]):
        self.k2v = dict(zip(keys, values))
        encoded = Counter()
        for w in dictionary:
            try:
                e = ''.join(self.k2v[c] for c in w)
                encoded[e] += 1
            except KeyError:
                continue
        self.enc_counter = encoded

    def encrypt(self, word1: str) -> str:
        return ''.join(self.k2v[c] for c in word1)

    def decrypt(self, word2: str) -> int:
        return self.enc_counter.get(word2, 0)
# revisit
# revisit
