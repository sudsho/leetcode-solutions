class Solution:
    def evalRPN(self, tokens):
        """Evaluate an arithmetic expression in Reverse Polish Notation.

        Scan left to right with a stack. Push numbers; on an operator pop the
        two most recent operands, apply it, and push the result back. The last
        value left on the stack is the answer. Division truncates toward zero,
        which is what int(a / b) gives for mixed signs (unlike Python's //)."""
        ops = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: int(a / b),  # truncate toward zero
        }
        stack = []
        for tok in tokens:
            if tok in ops:
                b = stack.pop()
                a = stack.pop()
                stack.append(ops[tok](a, b))
            else:
                stack.append(int(tok))
        return stack[0]
