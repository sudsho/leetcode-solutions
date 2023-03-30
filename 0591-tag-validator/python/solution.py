class Solution:
    def isValid(self, code: str) -> bool:
        n = len(code)
        if n < 2 or code[0] != '<':
            return False
        stack: list[str] = []
        i = 0
        while i < n:
            if not stack and i > 0:
                return False
            if code.startswith("<![CDATA[", i):
                end = code.find("]]>", i + 9)
                if end == -1:
                    return False
                i = end + 3
            elif code.startswith("</", i):
                end = code.find('>', i + 2)
                if end == -1:
                    return False
                tag = code[i + 2:end]
                if not stack or stack[-1] != tag or not self._valid_tag(tag):
                    return False
                stack.pop()
                i = end + 1
                if not stack and i != n:
                    return False
            elif code[i] == '<':
                end = code.find('>', i + 1)
                if end == -1:
                    return False
                tag = code[i + 1:end]
                if not self._valid_tag(tag):
                    return False
                stack.append(tag)
                i = end + 1
            else:
                i += 1
        return not stack

    def _valid_tag(self, tag: str) -> bool:
        return 1 <= len(tag) <= 9 and all(c.isupper() for c in tag)
