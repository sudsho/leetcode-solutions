class Solution:
    def intToRoman(self, num):
        # greedy: walk symbols from largest to smallest, including the
        # subtractive pairs (CM, CD, XC, XL, IX, IV) so we never need
        # to special-case them later
        pairs = [
            (1000, "M"), (900, "CM"),
            (500, "D"),  (400, "CD"),
            (100, "C"),  (90, "XC"),
            (50, "L"),   (40, "XL"),
            (10, "X"),   (9, "IX"),
            (5, "V"),    (4, "IV"),
            (1, "I"),
        ]
        out = []
        for val, sym in pairs:
            while num >= val:
                out.append(sym)
                num -= val
        return "".join(out)
