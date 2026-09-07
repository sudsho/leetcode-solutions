# 1163. Last Substring in Lexicographical Order

Difficulty: Hard
Topics  : Two-pointer suffix duel, and the proper-prefix case on the other side of the line

## Problem

Given a string `s`, return the substring of `s` that is greatest in
lexicographical order.

## Approach

The answer is a suffix. Any substring is a prefix of the suffix starting at the
same index, and a string is never smaller than its own proper prefix, so the
maximum over substrings is attained at a suffix. That reduces `O(n^2)`
candidates to `n`.

Two pointers duel over them. `i < j` are live candidates and `k` characters have
matched. On `s[i + k] > s[j + k]` the right candidate loses and `j` jumps to
`j + k + 1`; on `<` the left one loses and `i` jumps to `max(i + k + 1, j)`,
with `j` reset to `i + 1`. Each mismatch retires `k + 1` candidates for the
`k + 1` characters that were read, so the scan is `O(n)` time and `O(1)` extra
space.

The skip is the one thing that needs saying. If suffix `i` beats suffix `j` at
offset `k`, then every `t` in `[j, j + k]` is dead, because suffix `i + (t - j)`
agrees with suffix `t` inside the matched block and then splits where `i`'s side
is larger. So the loser plus the whole matched run goes at once.

## Why this problem

499 two nights ago put a stipulated tie-break into a Dijkstra key and found that
getting it there costs a proof. Dijkstra wants its key monotone under extension,
and lex order on strings is not: `"l" < "lu"` but `"ld" > "lud"`. The failure is
confined to pairs where one string is a proper prefix of the other, and on 499
those pairs could not arise, because two instruction strings were compared only
at equal distance and a proper prefix would have cost strictly less. The prefix
case was the entire difficulty and the other component of the key eliminated it.

This problem was picked because it is the same order with the same delicate case
and no way to rule it out. The candidates are suffixes of one string, so no two
have the same length, and suffix `j` is a proper prefix of suffix `i` as soon as
the string repeats enough for a match to run off the end.

## The prefix case, on the other side

It costs nothing here.

Nothing is extended. The candidates are complete strings, compared once, and lex
order on a finite set of complete strings is a total order whose maximum exists
however the prefixes fall. When suffix `j` is a proper prefix of suffix `i`, the
longer one wins and that is the answer - the same fact that broke monotonicity
on 499, pointing the other way.

So it is not the order and it is not the case. 499 needed the prefix pairs
impossible and this one lets them decide the answer, and what separates the two
nights is only whether the comparison has to survive an extension. That is the
distinction 499 proposed, tested somewhere it had not been tested, and it holds.

It is also not an edge case, which is what I expected it to be. `k > 0` at the
loop exit says the right candidate ran off the end mid-match, which is exactly
the prefix case, and the `__main__` run counts it over 1000 random strings of
length 200:

```
  |alphabet|= 2  ended mid-match  502/1000
  |alphabet|= 3  ended mid-match  323/1000
  |alphabet|=26  ended mid-match   48/1000
```

Half the time on a binary alphabet. `"banana"` is the small version - the two
candidates alive at the finish are `"nana"` and `"na"`. The exit needs no case
split even so: `s[i:]` is the answer whether the scan ended by exhausting `j` or
by running out of string mid-match, and the two exits mean different things.

## The max in the skip, measured

`i = max(i + k + 1, j)` reads like a correctness guard and I had it filed as one.
It is not. `i + k + 1` is the first index the elimination argument does not kill,
but every index below `j` was already killed in an earlier round, so the left
pointer may as well jump to `j`. Dropping the max leaves the scan correct and
lets it re-eliminate.

Exhaustively: every binary string up to length 11 and every ternary string up to
length 7, and the unguarded version never returned a different answer.

What it does cost is the whole bound. On `("ba" * m) + "aabb"`:

```
  n=    8  guarded=     8 (n)   unguarded=     15   n*n/4-1=     15
  n=  104  guarded=   104 (n)   unguarded=   2703   n*n/4-1=   2703
  n=  404  guarded=   404 (n)   unguarded=  40803   n*n/4-1=  40803
```

Exactly `n` against exactly `n^2 / 4 - 1`, on a family where both agree about the
answer at every size. So the line is load-bearing and no part of the correctness
argument mentions it, which is 685's shape - a convention the code must respect
that the proof never sees - except that here what is at stake is the complexity
rather than the printed answer.

## Bounds

The answer's length is `n - i` where `i` is the winner, so it runs from `1` (the
last character wins, as in `"abc"`) to `n` (the whole string wins, which happens
exactly when `s` is the maximum of its own suffixes - `"zzzzz"`, `"a"`). The
number of live candidates is `n` and each mismatch retires at least one, which is
the crude termination argument; the `k + 1` version is what makes it linear
rather than quadratic. `j + k` never decreases in the guarded version, and that
is the invariant the unguarded one gives up.

## Files

- `python/solution.py`
