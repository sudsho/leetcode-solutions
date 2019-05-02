# revisited - cleaned up
class Solution:
    def longestCommonPrefix(self, strs):
        if not strs:
            return ''
        # use the first string as the candidate prefix and shrink as needed
        prefix = strs[0]
        for s in strs[1:]:
            # shorten prefix until s starts with it
            while not s.startswith(prefix):
                prefix = prefix[:-1]
                if not prefix:
                    return ''
        return prefix
