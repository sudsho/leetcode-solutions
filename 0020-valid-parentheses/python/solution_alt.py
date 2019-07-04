# alt approach: naive replace-until-stable. slow but cute

class Solution:
    def isValid(self, s):
        # keep replacing pairs until nothing changes
        while '()' in s or '[]' in s or '{}' in s:
            s = s.replace('()','').replace('[]','').replace('{}','')
        return s == ''
