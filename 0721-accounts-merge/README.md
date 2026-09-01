# 721. Accounts Merge

Difficulty: Medium
Topics  : Union-find + what part of a printed answer is actually a choice

## Problem

Each account is `[name, email...]`. Two accounts belong to one person if they
share any email; a person may have many accounts, all under the same name.
Return the merged accounts as `[name, *sorted(emails)]`, in any order.

## Approach

Union-find over account indices, with a dict from each email to the first
account that claimed it - a second claim is the edge. Sharing an email is not
transitive, so the relation being quotiented by is its transitive closure, and
as in 1202 the edges can be discarded once merged since nothing downstream asks
which shared email caused a merge.

The reason this one is worth keeping is that the three parts of the output sit in
three different places. The partition is the quotient and is most of the answer.
The sorted email list is not a section at all - a class determines a set, and
sorting is a rendering convention on a determined object rather than a
representative picked from an orbit. The name is a member's copy of a field,
chosen arbitrarily and then printed, which by the observability rule ought to
need the kind of exchange argument 1202 needed; it needs none, because the name
is constant on classes. Observable and still free, since what is observed does
not vary across the thing being picked from.

`O(sum |A_i| * alpha + E log E)` for `E` distinct emails, the sort dominating.

## Files

- `python/solution.py`
