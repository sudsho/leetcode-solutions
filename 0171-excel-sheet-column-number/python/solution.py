class Solution:
    def titleToNumber(self, columnTitle):
        """Convert an Excel column title (A, B, ..., Z, AA, AB, ...) to its number.

        The titles are a bijective base-26 numeral system: the digits are
        A..Z standing for 1..26, and crucially there is no zero. That "no zero"
        is the only thing that makes this different from ordinary base-26 - AA is
        27, not 0, because each position runs 1..26 rather than 0..25.

        Reading left to right, every new character means the running total so far
        is one full "place" up, so multiply by 26 and add the current digit's
        value (ord(ch) - ord('A') + 1). Same shape as parsing a decimal string.
        """
        result = 0
        for ch in columnTitle:
            result = result * 26 + (ord(ch) - ord("A") + 1)
        return result


if __name__ == "__main__":
    s = Solution()
    assert s.titleToNumber("A") == 1
    assert s.titleToNumber("Z") == 26
    assert s.titleToNumber("AA") == 27
    assert s.titleToNumber("AB") == 28
    assert s.titleToNumber("ZY") == 701
    assert s.titleToNumber("FXSHRXW") == 2147483647
    print("all good")
