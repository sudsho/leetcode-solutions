from typing import List

class Solution:
    def oddEvenJumps(self, arr: List[int]) -> int:
        n = len(arr)
        odd_next = [0] * n
        even_next = [0] * n

        def fill(order: list[int]) -> list[int]:
            stack: list[int] = []
            res = [0] * n
            for i in order:
                while stack and stack[-1] < i:
                    res[stack.pop()] = i
                stack.append(i)
            return res

        order_asc = sorted(range(n), key=lambda i: (arr[i], i))
        odd_next = fill(order_asc)
        order_desc = sorted(range(n), key=lambda i: (-arr[i], i))
        even_next = fill(order_desc)

        odd = [False] * n
        even = [False] * n
        odd[-1] = even[-1] = True
        ans = 1
        for i in range(n - 2, -1, -1):
            j = odd_next[i]
            if j and even[j]:
                odd[i] = True
                ans += 1
            j = even_next[i]
            if j and odd[j]:
                even[i] = True
        return ans
