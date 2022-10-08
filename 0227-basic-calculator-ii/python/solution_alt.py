# iterator approach with peek
class Solution:
    def calculate(self, s: str) -> int:
        s = s.replace(" ", "") + "+"
        stack = []
        num = 0
        op = "+"
        for ch in s:
            if ch.isdigit():
                num = num * 10 + int(ch)
            else:
                if op == "+":
                    stack.append(num)
                elif op == "-":
                    stack.append(-num)
                elif op == "*":
                    stack[-1] *= num
                else:
                    last = stack.pop()
                    quotient = abs(last) // num
                    if last < 0:
                        quotient = -quotient
                    stack.append(quotient)
                op = ch
                num = 0
        return sum(stack)
