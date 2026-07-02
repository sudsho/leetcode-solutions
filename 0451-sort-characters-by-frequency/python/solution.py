from collections import Counter


class Solution:
    def frequencySort(self, s):
        """Sort characters by descending frequency.

        Count occurrences, then bucket characters by their count so we can read
        them off from the highest bucket down. Bucket sort avoids the O(k log k)
        comparison sort of the distinct characters; the number of buckets is
        bounded by len(s) since no char can appear more often than that.
        """
        counts = Counter(s)
        buckets = [[] for _ in range(len(s) + 1)]
        for char, freq in counts.items():
            buckets[freq].append(char)

        out = []
        for freq in range(len(s), 0, -1):
            for char in buckets[freq]:
                out.append(char * freq)
        return "".join(out)
