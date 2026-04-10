# Given a rotated sorted array (originally sorted, then rotated at an unknown pivot),
# search for a target value and return its index, or -1 if not found.
# Must run in O(log n) time — use modified binary search.

class Solution:
    def search(self, nums: list[int], target: int) -> int:
        lo, hi = 0, len(nums) - 1

        while lo <= hi:
            mid = (lo + hi) // 2

            if nums[mid] == target:
                return mid

            # Determine which half is sorted
            if nums[lo] <= nums[mid]:
                # Left half is sorted
                if nums[lo] <= target < nums[mid]:
                    hi = mid - 1
                else:
                    lo = mid + 1
            else:
                # Right half is sorted
                if nums[mid] < target <= nums[hi]:
                    lo = mid + 1
                else:
                    hi = mid - 1

        return -1

# Time:  O(log n) — binary search halves the search space each step
# Space: O(1)    — no extra memory used

if __name__ == "__main__":
    sol = Solution()
    print(sol.search([4, 5, 6, 7, 0, 1, 2], 0))   # 4
    print(sol.search([4, 5, 6, 7, 0, 1, 2], 3))   # -1
    print(sol.search([1], 0))                       # -1
