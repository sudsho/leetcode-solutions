class Solution:
    def fourSum(self, nums, target):
        nums.sort()
        n = len(nums)
        out = []
        for i in range(n - 3):
            if i > 0 and nums[i] == nums[i-1]:
                continue
            # prune
            if nums[i] + nums[i+1] + nums[i+2] + nums[i+3] > target:
                break
            if nums[i] + nums[n-1] + nums[n-2] + nums[n-3] < target:
                continue
            for j in range(i + 1, n - 2):
                if j > i + 1 and nums[j] == nums[j-1]:
                    continue
                if nums[i] + nums[j] + nums[j+1] + nums[j+2] > target:
                    break
                if nums[i] + nums[j] + nums[n-1] + nums[n-2] < target:
                    continue
                l, r = j + 1, n - 1
                need = target - nums[i] - nums[j]
                while l < r:
                    s = nums[l] + nums[r]
                    if s == need:
                        out.append([nums[i], nums[j], nums[l], nums[r]])
                        l += 1
                        r -= 1
                        while l < r and nums[l] == nums[l-1]:
                            l += 1
                        while l < r and nums[r] == nums[r+1]:
                            r -= 1
                    elif s < need:
                        l += 1
                    else:
                        r -= 1
        return out
