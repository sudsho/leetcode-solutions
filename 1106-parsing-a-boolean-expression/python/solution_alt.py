# recursive parser using index walker
class Solution:
    def parseBoolExpr(self, expression: str) -> bool:
        self._i = 0
        s = expression

        def parse() -> bool:
            ch = s[self._i]
            if ch == "t":
                self._i += 1
                return True
            if ch == "f":
                self._i += 1
                return False
            op = ch
            self._i += 2  # skip op and "("
            args = []
            args.append(parse())
            while s[self._i] == ",":
                self._i += 1
                args.append(parse())
            self._i += 1  # skip ")"
            if op == "!":
                return not args[0]
            if op == "&":
                return all(args)
            return any(args)

        return parse()
