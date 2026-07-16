class Solution:
    def fractionToDecimal(self, numerator, denominator):
        """Format numerator/denominator as a string, wrapping any repeat in ().

        The integer part is plain long division. The fractional part is the
        grade-school algorithm: multiply the remainder by 10, take the next
        digit, carry the new remainder. A fraction repeats exactly when a
        remainder we have already seen comes back around, so we remember the
        output position where each remainder first appeared. The moment a
        remainder repeats we splice a "(" in at that stored position and close
        with ")". A remainder of 0 means the decimal terminates.
        """
        if numerator == 0:
            return "0"

        result = []
        # XOR of the signs: exactly one negative operand -> negative result.
        if (numerator < 0) ^ (denominator < 0):
            result.append("-")

        n, d = abs(numerator), abs(denominator)
        integer, rem = divmod(n, d)
        result.append(str(integer))

        if rem == 0:
            return "".join(result)

        result.append(".")
        # Map each remainder to the index in `result` where its digit will land.
        seen = {}
        while rem and rem not in seen:
            seen[rem] = len(result)
            rem *= 10
            digit, rem = divmod(rem, d)
            result.append(str(digit))

        if rem:
            start = seen[rem]
            result.insert(start, "(")
            result.append(")")

        return "".join(result)
