class Solution:
    def parseBoolExpr(self, expression: str) -> bool:
        stack = []
        for ch in expression:
            if ch == ",":
                continue
            if ch == ")":
                operands = []
                while stack[-1] not in "!&|":
                    operands.append(stack.pop())
                op = stack.pop()
                stack.pop()  # the '('
                if op == "!":
                    stack.append(not operands[0])
                elif op == "&":
                    stack.append(all(operands))
                else:
                    stack.append(any(operands))
            elif ch == "t":
                stack.append(True)
            elif ch == "f":
                stack.append(False)
            else:
                stack.append(ch)
        return stack[-1]
