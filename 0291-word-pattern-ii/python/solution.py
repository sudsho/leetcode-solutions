class Solution:
    def wordPatternMatch(self, pattern: str, s: str) -> bool:
        # Try to build a bijection from pattern chars to non-empty substrings of
        # s by backtracking. At pattern[i] we either reuse the substring already
        # bound to that char (and require s to continue with it) or, if the char
        # is new, try every prefix of the remaining string as its binding.
        char_to_word: dict[str, str] = {}
        used_words: set[str] = set()  # keep the mapping injective

        def backtrack(i: int, j: int) -> bool:
            if i == len(pattern) and j == len(s):
                return True
            if i == len(pattern) or j == len(s):
                return False

            ch = pattern[i]
            if ch in char_to_word:
                word = char_to_word[ch]
                if not s.startswith(word, j):
                    return False
                return backtrack(i + 1, j + len(word))

            # New char: try each prefix s[j:k] as its binding.
            for k in range(j + 1, len(s) + 1):
                word = s[j:k]
                if word in used_words:
                    continue  # two pattern chars cannot share a word
                char_to_word[ch] = word
                used_words.add(word)
                if backtrack(i + 1, k):
                    return True
                # undo before trying a longer prefix
                del char_to_word[ch]
                used_words.discard(word)

            return False

        return backtrack(0, 0)
