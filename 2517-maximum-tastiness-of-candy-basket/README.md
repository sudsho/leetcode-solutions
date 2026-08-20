# 2517. Maximum Tastiness of Candy Basket

Difficulty: Medium
Topics  : array, greedy, binary search, sorting

## Problem

Pick `k` candies from `price`. The tastiness of the basket is the smallest absolute difference between any two candies in it. Maximise that. `k` may be `1`, in which case there are no pairs at all.

## Approach

Ninth on the monotone-predicate-plus-bisect shape, and the first where I had already written the predicate. This is 1552 with a different noun - there the greedy placed balls along a line keeping a minimum separation, here it picks candies along a line of prices keeping a minimum difference. Same scan, same monotonicity, same direction. I went looking for the part that was new and there is not one, in the algorithm.

So the day only pays if the repeat exposes something, and it does, in the place yesterday left open.

Yesterday's note closed with a three-way split: the search space is generically bigger than the answer set, and there are three things you can do about it - repair it at the boundary (719, the jump in the count), replace it with the answer set (1482 by luck, 2616 by argument), or leave it alone because the answer set is finite and hopeless anyway (774). And the property deciding which is available is the **size** of the answer set.

## The correction

This problem's answer set is every pairwise difference: the answer is the tight gap inside the chosen basket, so it is `price[b] - price[a]` for some pair. Attained, same as 2616. The difference is how many candidates that is - `n - 1` there, because the exchange argument collapsed the pairing down to adjacent positions, and `n(n-1)/2` here, because the basket is a subsequence and any two of its members can be the tight one.

At the constraint ceiling `n = 2e4` that is `2e8` candidates. Against 30 predicate calls for bisecting the range.

Which is where the split breaks. I had filed 774 under *finite but hopeless* as though hopeless were a property of the number - two billion, self-evidently too many. It is not. This set is smaller than 774's by a factor of five and it is still 600 times worse than not building it, because the plain range search only ever costs `log(1e9)`. And 2616's `n - 1` was never a win for being small. It was a win for beating `log(max - min)` on that input.

**So the deciding property is not the answer set's size. It is its size against the cost of the search it would replace.** The three-way split is two branches and a comparison, and the hopeless branch was never separate - 774 is this problem with a worse constant.

Two days running now that something I was treating as a property of the problem turned out to be relative to something outside it. Yesterday canonicity turned out to be relative to the representation. Today enumerability turns out to be relative to the alternative. I do not think that is a coincidence so much as what happens when you take an adjective off a checklist and never ask *compared to what*.

The candidate-space search is still in the file, behind a `limit` that makes it decline rather than quietly cost `O(n^2)`. It is a test fixture, not a competing implementation, and it does test one thing the primary cannot test on itself: that the answer really does land on a pairwise difference.

## The predicate, and the bound

The greedy is 1552's and the exchange argument is one line - if a larger basket declines the candy the greedy takes at `i`, its own next pick is some `j > i`, and swapping it for `i` keeps every later gap at least as large since `price[i] <= price[j]`. Third of nine predicates with a trivial inner greedy, which is what I claimed after 1482 was the pattern and then withdrew after 2616 stacked two real exchange arguments into one predicate. Both readings survive: the variation in this shape is all in the predicate, and the predicate is sometimes free.

Direction: maximisation, so the true half keeps `mid` and `mid` rounds **up**. Third maximisation in nine, after 1552 and 1898, so this is not the flip catching me out that it was on the 10th. Fourth day writing the rule out anyway.

Bounds, fifth day running, and this time the test threw out my reason. I wrote the top as *gap `max - min` admits the two ends and nothing between them, count exactly 2*, and `[7, 7, 7, 7]` has span `0`, where top and bottom are the same point and the count is `4`. The bound survives - no basket has a gap above `max - min` because no pair does, and that argument never mentioned the count. But it survives for a reason other than the one I gave it. The last four days the missing bound argument was at least visibly missing. This one was present and wrong, which is worse.

`k == 1` is a hole in the statement: it asks for the minimum over the pairs of a one-element basket, of which there are none. Taking the empty minimum as `0` rather than letting the search run, which would return `max - min` for no defensible reason. Third boundary hole in the run and the first I caught by reading rather than from a failing test.

## The witness

Fifteenth day of the summary-versus-set split, and the first in a while that confirms the rule rather than moving it.

Back on the 11th I called slack a reason a witness fails to be canonical. On the 17th I decided it was a confound, because every slack case in that stretch happened to be symmetric too. That was an inference from absence and I have not had the case that separates them - until this one.

`[1, 2, 5, 8, 13, 21]` with `k = 3` answers `8`, and both `(1, 13, 21)` and `(2, 13, 21)` achieve it. Two members in the witness set, all prices distinct, nothing interchangeable, no symmetry anywhere. Pure slack. And the leftmost greedy still names one of them.

So slack does not remove the distinguished element, and the 17th was right. Six days that looked otherwise were six days that were also symmetric.

Ties in `price` bring back 2616's other half unchanged - equal candies are interchangeable, a stable sort picks between them by input order, and in original-index space no basket is canonical. Same two tests as yesterday on a witness that is a subsequence instead of a set of pairs.

## Complexity

Primary: `O(n log n)` to sort, `O(n log(max - min))` for the search. Candidate form: `O(n^2 log n)` to build and sort the differences, then `O(n log n)` - refuses above `limit`. Witness: primary plus one scan. `k == 2`: one pass.

## Files

- `python/solution.py`
