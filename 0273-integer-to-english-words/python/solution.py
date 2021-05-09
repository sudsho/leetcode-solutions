class Solution:
    UNDER_20 = [
        "", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine",
        "Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen",
        "Sixteen", "Seventeen", "Eighteen", "Nineteen",
    ]
    TENS = [
        "", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety",
    ]
    THOUSANDS = ["", "Thousand", "Million", "Billion"]

    def numberToWords(self, num: int) -> str:
        if num == 0:
            return "Zero"

        def below_1000(n: int) -> str:
            if n == 0:
                return ""
            if n < 20:
                return self.UNDER_20[n] + " "
            if n < 100:
                return self.TENS[n // 10] + " " + below_1000(n % 10)
            return self.UNDER_20[n // 100] + " Hundred " + below_1000(n % 100)

        out, i = "", 0
        while num > 0:
            if num % 1000:
                out = below_1000(num % 1000) + self.THOUSANDS[i] + " " + out
            num //= 1000
            i += 1
        return out.strip()
