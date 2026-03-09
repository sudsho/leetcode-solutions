from typing import List


class Solution:
    def maxDifference(self, s: str, k: int) -> int:
        # for each pair of distinct digits a (must be odd freq), b (must be even, > 0),
        # find max f_a(window) - f_b(window) with |window| >= k.
        # use prefix counts; with parity-pair (pa, pb) of (cnt_a, cnt_b) at boundaries,
        # we want substring [l, r) with pa[r]-pa[l] odd, pb[r]-pb[l] even, pb[r]-pb[l] > 0, r-l >= k.
        # for each (a, b), iterate r and keep min of pa[l]-pb[l] across valid l with matching parity.
        # valid l: parity(pa[l]) != parity(pa[r]) (so diff odd), parity(pb[l]) == parity(pb[r]) (so diff even),
        # pb[l] < pb[r] (so b appears at least once), and r - l >= k.
        n = len(s)
        ans = -10**9
        digits = list({c for c in s})
        # prefix arrays per digit
        pref = {d: [0] * (n + 1) for d in "01234"}
        for i, c in enumerate(s):
            for d in pref:
                pref[d][i + 1] = pref[d][i] + (1 if c == d else 0)
        for a in digits:
            for b in digits:
                if a == b:
                    continue
                pa = pref[a]
                pb = pref[b]
                # for each parity pair (par_pa_l, par_pb_l), keep min (pa[l] - pb[l]) over l <= r - k
                # and pb[l] < pb[r]. Encoding (par_pa_l in 0/1, par_pb_l in 0/1) = 4 buckets.
                # Each bucket also needs to filter pb[l] < pb[r]; we drop entries where pb[l] >= current pb[r].
                # Simple approach: for each parity pair, store list of (pb[l], pa[l]-pb[l]) and use a running min
                # split by pb[l] value; since pb is non-decreasing, "pb[l] < pb[r]" is equivalent to "l <= last index where pb increased before pb[r]".
                # We add entries lazily: when pb[r] strictly increases, all queued entries from index <= r-k can be processed.
                bucket_min = [10**9, 10**9, 10**9, 10**9]
                pending = []  # list of (idx, pb_val, key, parity_pair)
                last_pb = 0
                last_pb_idx = 0  # index where pb last strictly increased
                # track separately
                # simpler: for each r, l candidates are 0..r-k. For each such l, parity_pair = (pa[l]&1, pb[l]&1).
                # require pb[l] < pb[r]. Buckets keyed by parity pair, but we only use l's whose pb[l] < pb[r].
                # since pb is non-decreasing, valid l's are those with l < first index where pb >= pb[r].
                # Equivalently, l < smallest i with pb[i] == pb[r] when pb just became pb[r], i.e. up to last_increase_index.
                # So we eagerly admit l = r - k into bucket whenever pb[r] > pb[l]; otherwise keep waiting.
                # To keep it simple in this implementation, recompute valid l's via two pointers.
                # right pointer r ranges in [k, n]; left admit pointer l_admit moves forward.
                l_admit = 0  # next l to consider
                for r in range(k, n + 1):
                    # admit all l up to r - k whose pb[l] < pb[r]
                    while l_admit <= r - k and pb[l_admit] < pb[r]:
                        ppa = pa[l_admit] & 1
                        ppb = pb[l_admit] & 1
                        key = pa[l_admit] - pb[l_admit]
                        idx = ppa * 2 + ppb
                        if key < bucket_min[idx]:
                            bucket_min[idx] = key
                        l_admit += 1
                    # to track validity correctly when pb[r] grows we shouldn't admit; we admit only those l with pb[l] < pb[r].
                    # at this point bucket_min contains min over l <= r - k with pb[l] < pb[r].
                    # we need parity_pair (par_pa_l, par_pb_l) = (par_pa_r XOR 1, par_pb_r), so:
                    par_pa_r = pa[r] & 1
                    par_pb_r = pb[r] & 1
                    target_pa_l = par_pa_r ^ 1
                    target_pb_l = par_pb_r
                    idx = target_pa_l * 2 + target_pb_l
                    if bucket_min[idx] < 10**9:
                        cand = (pa[r] - pb[r]) - bucket_min[idx]
                        if cand > ans:
                            ans = cand
                    # if pb[r] is about to be larger next iter, bucket_min might miss valid l where pb[l] < pb[r+1] but pb[l] == pb[r]
                    # those l's were skipped above; but they will be admitted next iter when pb[r+1] > pb[l]. so okay.
                # if no valid window at all, return 0 (problem usually guarantees existence; defensive)
        return ans if ans > -10**8 else 0

# refactored: cleaned up 3445
