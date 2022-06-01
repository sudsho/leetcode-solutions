class Solution:
    def calculate(self, s: str) -> int:
        stack = []
        num = 0
        op = "+"
        s += "+"
        for ch in s:
            if ch.isdigit():
                num = num * 10 + int(ch)
            elif ch in "+-*/":
                if op == "+":
                    stack.append(num)
                elif op == "-":
                    stack.append(-num)
                elif op == "*":
                    stack.append(stack.pop() * num)
                else:
                    last = stack.pop()
                    stack.append(int(last / num))
                op = ch
                num = 0
        return sum(stack)
