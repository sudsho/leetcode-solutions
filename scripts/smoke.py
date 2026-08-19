#!/usr/bin/env python3
"""Offline smoke test for the leetcode-solutions portfolio.

This repo is a collection of LeetCode solutions (one folder per problem,
each with python/solution.py exposing a class Solution). There is nothing
to "run" end to end, so the smoke instead loads a representative batch of
solution modules and checks each against known input/output cases.

It reports pass/fail per problem and exits 0 only if every sampled
solution produces the expected answers. Pure Python, no downloads, no
third-party dependencies.

Usage:
    python scripts/smoke.py
"""

import importlib.util
import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_solution(problem_dir):
    """Load class Solution from <problem_dir>/python/solution.py by path.

    Directory names start with digits and contain hyphens, so they are not
    importable as normal modules; we load the file directly instead.
    """
    path = os.path.join(REPO_ROOT, problem_dir, "python", "solution.py")
    if not os.path.isfile(path):
        raise FileNotFoundError(path)
    mod_name = "sol_" + problem_dir.replace("-", "_")
    spec = importlib.util.spec_from_file_location(mod_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if not hasattr(module, "Solution"):
        raise AttributeError("no class Solution in " + path)
    return module.Solution


# Each case is a callable that takes a fresh Solution instance and returns
# (actual, expected). This keeps in-place mutation problems easy to express:
# the callable sets up the input, calls the method, and reports whatever is
# observable (return value and/or the mutated buffer).

def c_two_sum(s):
    return s.twoSum([2, 7, 11, 15], 9), [0, 1]


def c_reverse_integer(s):
    return s.reverse(-123), -321


def c_palindrome_number(s):
    return (s.isPalindrome(121), s.isPalindrome(-121)), (True, False)


def c_roman_to_int(s):
    return s.romanToInt("MCMXCIV"), 1994


def c_longest_common_prefix(s):
    return s.longestCommonPrefix(["flower", "flow", "flight"]), "fl"


def c_valid_parentheses(s):
    return (s.isValid("()[]{}"), s.isValid("(]")), (True, False)


def c_remove_duplicates(s):
    nums = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]
    k = s.removeDuplicates(nums)
    return (k, nums[:k]), (5, [0, 1, 2, 3, 4])


def c_remove_element(s):
    nums = [3, 2, 2, 3]
    k = s.removeElement(nums, 3)
    return (k, sorted(nums[:k])), (2, [2, 2])


def c_search_insert(s):
    return s.searchInsert([1, 3, 5, 6], 5), 2


def c_max_subarray(s):
    return s.maxSubArray([-2, 1, -3, 4, -1, 2, 1, -5, 4]), 6


def c_plus_one(s):
    return s.plusOne([1, 2, 9]), [1, 3, 0]


def c_climb_stairs(s):
    return s.climbStairs(5), 8


def c_max_profit(s):
    return s.maxProfit([7, 1, 5, 3, 6, 4]), 5


def c_valid_palindrome(s):
    return (
        s.isPalindrome("A man, a plan, a canal: Panama"),
        s.isPalindrome("race a car"),
    ), (True, False)


def c_single_number(s):
    return s.singleNumber([4, 1, 2, 1, 2]), 4


def c_majority_element(s):
    return s.majorityElement([2, 2, 1, 1, 1, 2, 2]), 2


def c_contains_duplicate(s):
    return (
        s.containsDuplicate([1, 2, 3, 1]),
        s.containsDuplicate([1, 2, 3, 4]),
    ), (True, False)


def c_valid_anagram(s):
    return (
        s.isAnagram("anagram", "nagaram"),
        s.isAnagram("rat", "car"),
    ), (True, False)


def c_missing_number(s):
    return s.missingNumber([3, 0, 1]), 2


def c_move_zeroes(s):
    nums = [0, 1, 0, 3, 12]
    s.moveZeroes(nums)
    return nums, [1, 3, 12, 0, 0]


def c_reverse_string(s):
    buf = list("hello")
    s.reverseString(buf)
    return buf, list("olleh")


def c_fizz_buzz(s):
    return s.fizzBuzz(5), ["1", "2", "Fizz", "4", "Buzz"]


def c_fib(s):
    return s.fib(10), 55


def c_binary_search(s):
    return (
        s.search([-1, 0, 3, 5, 9, 12], 9),
        s.search([-1, 0, 3, 5, 9, 12], 2),
    ), (4, -1)


def c_length_of_last_word(s):
    return s.lengthOfLastWord("   fly me   to   the moon  "), 4


def c_str_str(s):
    return (s.strStr("sadbutsad", "sad"), s.strStr("leetcode", "leeto")), (0, -1)


def c_merge_sorted_array(s):
    nums1 = [1, 2, 3, 0, 0, 0]
    s.merge(nums1, 3, [2, 5, 6], 3)
    return nums1, [1, 2, 2, 3, 5, 6]


# problem_dir -> case callable. Order roughly by problem number.
CASES = [
    ("0001-two-sum", c_two_sum),
    ("0007-reverse-integer", c_reverse_integer),
    ("0009-palindrome-number", c_palindrome_number),
    ("0013-roman-to-integer", c_roman_to_int),
    ("0014-longest-common-prefix", c_longest_common_prefix),
    ("0020-valid-parentheses", c_valid_parentheses),
    ("0026-remove-duplicates-from-sorted-array", c_remove_duplicates),
    ("0027-remove-element", c_remove_element),
    ("0028-implement-strstr", c_str_str),
    ("0035-search-insert-position", c_search_insert),
    ("0053-maximum-subarray", c_max_subarray),
    ("0058-length-of-last-word", c_length_of_last_word),
    ("0066-plus-one", c_plus_one),
    ("0070-climbing-stairs", c_climb_stairs),
    ("0088-merge-sorted-array", c_merge_sorted_array),
    ("0121-best-time-to-buy-and-sell-stock", c_max_profit),
    ("0125-valid-palindrome", c_valid_palindrome),
    ("0136-single-number", c_single_number),
    ("0169-majority-element", c_majority_element),
    ("0217-contains-duplicate", c_contains_duplicate),
    ("0242-valid-anagram", c_valid_anagram),
    ("0268-missing-number", c_missing_number),
    ("0283-move-zeroes", c_move_zeroes),
    ("0344-reverse-string", c_reverse_string),
    ("0412-fizz-buzz", c_fizz_buzz),
    ("0509-fibonacci-number", c_fib),
    ("0704-binary-search", c_binary_search),
]


def run_case(problem_dir, case_fn):
    """Return (ok, detail) for a single problem case."""
    try:
        Solution = load_solution(problem_dir)
        actual, expected = case_fn(Solution())
    except Exception as exc:  # noqa: BLE001 - smoke wants to report, not crash
        return False, "error: {}: {}".format(type(exc).__name__, exc)
    if actual == expected:
        return True, "expected={!r}".format(expected)
    return False, "expected={!r} got={!r}".format(expected, actual)


def main():
    print("leetcode-solutions offline smoke")
    print("running {} sampled solutions from {}".format(len(CASES), REPO_ROOT))
    print("-" * 60)
    passed = 0
    failed = 0
    for problem_dir, case_fn in CASES:
        ok, detail = run_case(problem_dir, case_fn)
        status = "PASS" if ok else "FAIL"
        print("[{}] {:45s} {}".format(status, problem_dir, detail))
        if ok:
            passed += 1
        else:
            failed += 1
    print("-" * 60)
    print("total={} passed={} failed={}".format(len(CASES), passed, failed))
    if failed:
        print("SMOKE FAILED")
        return 1
    print("SMOKE PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
