class Solution:
    def removeDuplicateLetters(self, s):
        """Smallest-lexicographic string keeping one copy of each distinct char.

        Greedy monotonic stack. We want the result as small as possible, so when
        the current char is smaller than the char on top of the stack, we pop the
        top - but only if that top appears again later (otherwise dropping it now
        loses our only chance to include it). last[c] gives the final index of c,
        so `last[top] > i` is the "we'll see it again" test. A seen-set stops us
        from pushing a character that is already in the result.
        """
        last = {c: i for i, c in enumerate(s)}
        stack = []
        in_stack = set()
        for i, c in enumerate(s):
            if c in in_stack:
                continue
            while stack and stack[-1] > c and last[stack[-1]] > i:
                in_stack.discard(stack.pop())
            stack.append(c)
            in_stack.add(c)
        return "".join(stack)
