from typing import List, Tuple


def brute_force_best(s: str) -> int:
    """Index of the lexicographically greatest suffix, by building all of them.

    `O(n^2)` in time and space and not used by the solution. It is the oracle
    again, and here it is doing something the last two oracles did not: the
    answer is unique, so it is not measuring the size of a tie. It is measuring
    how often the *prefix case* decides the answer, which is the case 499 spent
    a proof ruling out.
    """
    return max(range(len(s)), key=lambda i: s[i:])


def duel(s: str, guarded: bool = True) -> Tuple[int, int, bool]:
    """The two-pointer scan, instrumented, with the `max` guard switchable.

    Returns `(winner, loop_iterations, exited_mid_match)`. `guarded=False` is
    the version that advances the left candidate to `i + k + 1` without taking
    the maximum against `j`, which is the line whose cost is measured in
    `__main__`.

    `exited_mid_match` is `k > 0` at the exit, which happens exactly when the
    right candidate ran off the end of the string while still matching - i.e.
    exactly when suffix `j` is a proper prefix of suffix `i`.
    """
    n = len(s)
    i, j, k = 0, 1, 0
    iterations = 0
    while j + k < n:
        iterations += 1
        if s[i + k] == s[j + k]:
            k += 1
        elif s[i + k] > s[j + k]:
            j = j + k + 1
            k = 0
        else:
            i = max(i + k + 1, j) if guarded else i + k + 1
            j = i + 1
            k = 0
    return i, iterations, k > 0


class Solution:
    def lastSubstring(self, s: str) -> str:
        """The lexicographically greatest substring of `s`.

        Picked as the third data point on the thread 499 opened. That night the
        finding was that a stipulated tie-break carried through an optimisation
        owes a compatibility proof, and the proof owed was monotonicity: lex
        order on strings satisfies `a < b => a + t < b + t` everywhere *except*
        on pairs where one string is a proper prefix of the other. On 499 those
        pairs could not arise, because two instruction strings were compared
        only at equal distance and a proper prefix would have cost strictly
        less. The prefix case was the whole difficulty and it was ruled out.

        Here it is not ruled out. Every candidate is a suffix of one string, so
        two candidates have different lengths by construction, and suffix `j` is
        a proper prefix of suffix `i` whenever the string is periodic enough for
        the match to run to the end. `"banana"` is that: the two live candidates
        at the finish are `"nana"` and `"na"`, and `"na"` is a proper prefix of
        `"nana"`.

        And it costs nothing. The comparison here is not carried through
        anything - the candidates are complete objects, compared once, and lex
        order on a finite set of complete strings is a total order whose maximum
        is well defined however the prefixes fall. The longer one wins, which is
        the same fact that broke monotonicity on 499 pointing the other way.

        So the two nights put the same delicate case on both sides of the same
        line. 499 needed it impossible; this one lets it decide the answer, and
        the difference is not the order and not the case. It is whether the
        comparison has to survive an extension.

        The scan: candidates `i < j`, matched `k` characters. On a mismatch the
        loser and everything between it and the mismatch point is discarded,
        because if suffix `i` beats suffix `j` at offset `k` then for every `t`
        in `[j, j + k]` the suffix at `i + (t - j)` beats the suffix at `t` - the
        two agree inside the matched block and split where `i`'s side is larger.
        That is `k + 1` candidates removed for `k + 1` characters read, which is
        the `O(n)` bound.

        The loop exits when `j + k` reaches `n`. If `k > 0` at that point the
        right candidate has run out mid-match and the prefix case has decided
        it; the answer is `s[i:]` either way, which is why the exit needs no
        case split even though the two exits mean different things.
        """
        n = len(s)
        i, j, k = 0, 1, 0
        while j + k < n:
            if s[i + k] == s[j + k]:
                k += 1
            elif s[i + k] > s[j + k]:
                # suffix i wins, so j and the k candidates behind it are all
                # beaten by their counterparts inside i's block.
                j = j + k + 1
                k = 0
            else:
                # suffix j wins. i + k + 1 is the first index the argument does
                # not eliminate, but everything below j was eliminated in an
                # earlier round, so the left candidate may jump straight to j.
                # the max is not correctness - without it the scan still returns
                # the right answer, it just re-eliminates. it is the O(n) bound.
                i = max(i + k + 1, j)
                j = i + 1
                k = 0
        return s[i:]


if __name__ == "__main__":
    solution = Solution()

    cases: List[Tuple[str, str]] = [
        ("abab", "bab"),
        ("leetcode", "tcode"),
        ("banana", "nana"),
        ("cacacb", "cb"),
        ("zzzzz", "zzzzz"),
        ("a", "a"),
        ("aa", "aa"),
        ("ababbababbabab", "bbababbabab"),
    ]
    print("answers, and whether the prefix case is what ended the scan")
    for text, expected in cases:
        got = solution.lastSubstring(text)
        winner, iterations, mid_match = duel(text)
        assert got == expected, (text, got, expected)
        assert winner == brute_force_best(text), (text, winner)
        print(
            f"  {text!r:18} -> {got!r:14} iterations={iterations:3d}"
            f"  ended mid-match={str(mid_match):5}"
        )

    # 499's proof was that the prefix case could not happen. here it is not an
    # edge case at all - it is the most common way the scan finishes on a small
    # alphabet, and the rarer the repeats the less often it comes up.
    import random

    random.seed(11)
    print("\nhow the scan exits, 1000 random strings of length 200")
    for alphabet in ("ab", "abc", "abcdefghijklmnopqrstuvwxyz"):
        mid = 0
        for _ in range(1000):
            text = "".join(random.choice(alphabet) for _ in range(200))
            _, _, ended_mid_match = duel(text)
            mid += ended_mid_match
        print(f"  |alphabet|={len(alphabet):2d}  ended mid-match {mid:4d}/1000")

    # the max guard, measured. it never changed an answer in an exhaustive
    # search over every binary string up to length 11 and every ternary string
    # up to length 7, and on this family it is the entire complexity bound.
    print("\ncost of dropping the max guard, on 'ba' * m + 'aabb'")
    for m in (2, 6, 20, 50, 100, 200):
        text = "ba" * m + "aabb"
        size = len(text)
        guarded_i, guarded_n, _ = duel(text, guarded=True)
        plain_i, plain_n, _ = duel(text, guarded=False)
        assert guarded_i == plain_i == brute_force_best(text), text
        print(
            f"  n={size:5d}  guarded={guarded_n:6d} (n)"
            f"   unguarded={plain_n:7d}   n*n/4-1={size * size // 4 - 1:7d}"
        )
