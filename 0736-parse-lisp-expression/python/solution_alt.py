class Solution:
    # Tokenizer + iterative evaluator using explicit env stack
    def evaluate(self, expression: str) -> int:
        i = 0
        n = len(expression)

        def parse_token() -> str | int:
            nonlocal i
            j = i
            while j < n and expression[j] not in ' ()':
                j += 1
            tok = expression[i:j]
            i = j
            if tok.lstrip('-').isdigit():
                return int(tok)
            return tok

        def eat(c: str) -> None:
            nonlocal i
            assert expression[i] == c
            i += 1

        def evaluate_expr(env: list[dict[str, int]]) -> int:
            nonlocal i
            if expression[i] != '(':
                tok = parse_token()
                if isinstance(tok, int):
                    return tok
                for s in reversed(env):
                    if tok in s:
                        return s[tok]
                return 0
            eat('(')
            head = parse_token()
            if expression[i] == ' ':
                i += 1
            if head == 'add' or head == 'mult':
                a = evaluate_expr(env)
                if expression[i] == ' ':
                    i += 1
                b = evaluate_expr(env)
                eat(')')
                return a + b if head == 'add' else a * b
            env.append({})
            try:
                while True:
                    if expression[i] == '(':
                        result = evaluate_expr(env)
                        eat(')')
                        return result
                    name_or_val = parse_token()
                    if expression[i] == ')':
                        eat(')')
                        if isinstance(name_or_val, int):
                            return name_or_val
                        for s in reversed(env):
                            if name_or_val in s:
                                return s[name_or_val]
                        return 0
                    if expression[i] == ' ':
                        i += 1
                    val = evaluate_expr(env)
                    env[-1][name_or_val] = val
                    if expression[i] == ' ':
                        i += 1
            finally:
                env.pop()

        return evaluate_expr([{}])
