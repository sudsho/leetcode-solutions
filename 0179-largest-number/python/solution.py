from functools import cmp_to_key


class Solution:
    def largestNumber(self, nums):
        """Arrange the numbers so their concatenation is the largest possible.

        The natural instinct - sort descending by value - is wrong: [3, 30]
        should become "330", not "303", yet 30 > 3 numerically. What actually
        matters for any pair (a, b) is which ordering of the two strings reads
        larger, i.e. compare a+b against b+a. That comparator is a valid total
        order (it's transitive on the string concatenations), so sorting the
        whole list by it yields the globally optimal arrangement.
        """
        strs = [str(n) for n in nums]

        def compare(a, b):
            # Put whichever of a+b / b+a is the bigger string first.
            if a + b > b + a:
                return -1
            if a + b < b + a:
                return 1
            return 0

        strs.sort(key=cmp_to_key(compare))

        # All-zero input (e.g. [0, 0]) would otherwise render as "00"; collapse
        # any leading-zero result to a single "0".
        if strs[0] == "0":
            return "0"
        return "".join(strs)


if __name__ == "__main__":
    s = Solution()
    assert s.largestNumber([10, 2]) == "210"
    assert s.largestNumber([3, 30, 34, 5, 9]) == "9534330"
    assert s.largestNumber([0, 0]) == "0"
    assert s.largestNumber([1]) == "1"
    assert s.largestNumber([432, 43, 43]) == "4343432"
    print("all cases pass")
