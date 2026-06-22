class Solution:
    def majorityElement(self, nums):
        """Return every element appearing more than floor(n/3) times.

        Problem 169 used Boyer-Moore voting to find the single > n/2 element.
        The key observation that generalizes it: there can be at most two
        values that occur more than n/3 times (three such values would already
        account for more than n elements). So we track two candidates and two
        counts simultaneously.

        The voting loop has three cases per element, checked in order:
          1. it matches an existing candidate -> bump that count
          2. some candidate slot is empty (count 0) -> adopt the element there
          3. neither -> the element cancels one unit from *both* candidates

        Case 3 is the heart of it: an element that is neither candidate pairs
        off against one vote of each, mirroring how the n/2 version cancels
        unequal pairs. Whatever survives with positive count is only a
        *possible* answer, so a second pass verifies the true frequencies
        before returning them.
        """
        cand1, cand2 = None, None
        count1, count2 = 0, 0

        for x in nums:
            if cand1 is not None and x == cand1:
                count1 += 1
            elif cand2 is not None and x == cand2:
                count2 += 1
            elif count1 == 0:
                cand1, count1 = x, 1
            elif count2 == 0:
                cand2, count2 = x, 1
            else:
                count1 -= 1
                count2 -= 1

        # The survivors are only candidates; confirm they clear the n/3 bar.
        threshold = len(nums) // 3
        result = []
        for c in (cand1, cand2):
            if c is not None and nums.count(c) > threshold:
                result.append(c)
        return result


if __name__ == "__main__":
    s = Solution()
    assert sorted(s.majorityElement([3, 2, 3])) == [3]
    assert sorted(s.majorityElement([1])) == [1]
    assert sorted(s.majorityElement([1, 2])) == [1, 2]
    assert sorted(s.majorityElement([1, 1, 1, 3, 3, 2, 2, 2])) == [1, 2]
    print("all cases pass")
