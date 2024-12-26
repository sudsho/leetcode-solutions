class Solution:
    def evaluate(self, expression: str) -> int:
        scope: list[dict[str, int]] = [{}]

        def lookup(name: str) -> int:
            for s in reversed(scope):
                if name in s:
                    return s[name]
            return 0

        def parse_value(token: str) -> int:
            if token.lstrip("-").isdigit():
                return int(token)
            return lookup(token)

        def split(expr: str) -> list[str]:
            tokens: list[str] = []
            depth = 0
            buf: list[str] = []
            for ch in expr:
                if ch == "(":
                    depth += 1
                    buf.append(ch)
                elif ch == ")":
                    depth -= 1
                    buf.append(ch)
                elif ch == " " and depth == 0:
                    tokens.append("".join(buf))
                    buf = []
                else:
                    buf.append(ch)
            if buf:
                tokens.append("".join(buf))
            return tokens

        def evalu(expr: str) -> int:
            if not expr.startswith("("):
                return parse_value(expr)
            inner = expr[1:-1]
            head, _, rest = inner.partition(" ")
            if head == "add":
                a, b = split(rest)
                return evalu(a) + evalu(b)
            if head == "mult":
                a, b = split(rest)
                return evalu(a) * evalu(b)
            scope.append({})
            tokens = split(rest)
            for i in range(0, len(tokens) - 1, 2):
                name = tokens[i]
                val = evalu(tokens[i + 1])
                scope[-1][name] = val
            result = evalu(tokens[-1])
            scope.pop()
            return result

        return evalu(expression)
# tightened naming
