class Solution:
    def reverseBits(self, n):
        """Reverse the bits of a 32-bit unsigned integer.

        Pull the low bit off n each step and shift it onto the result from the
        left, so the last bit read ends up in the least significant position.
        """
        result = 0
        for _ in range(32):
            result = (result << 1) | (n & 1)
            n >>= 1
        return result

    def reverseBits_byte_table(self, n):
        """Same result, reversing one byte at a time via a precomputed table.

        Reversing 8 bits is a single lookup, so a full word costs four lookups
        plus shifts - worth it when reverseBits is called in a hot loop.
        """
        table = [self._reverse_byte(b) for b in range(256)]
        result = 0
        for shift in (0, 8, 16, 24):
            byte = (n >> shift) & 0xFF
            result |= table[byte] << (24 - shift)
        return result

    @staticmethod
    def _reverse_byte(b):
        r = 0
        for _ in range(8):
            r = (r << 1) | (b & 1)
            b >>= 1
        return r
