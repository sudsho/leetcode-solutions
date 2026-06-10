# unique binary search trees - count how many structurally distinct BSTs can
# store the values 1..n. The key observation: if we fix value i as the root,
# the i-1 smaller values form the left subtree and the n-i larger values form
# the right subtree, independently. So the total is a sum over the choice of
# root - which is exactly the Catalan number recurrence.

class Solution:
    def numTrees(self, n):
        # dp[k] = number of unique BSTs buildable from k distinct ordered values.
        # dp[0] = 1 because the empty tree counts as a single valid shape.
        dp = [0] * (n + 1)
        dp[0] = 1
        for nodes in range(1, n + 1):
            # try every value as the root; left gets root-1 nodes, right the rest
            for root in range(1, nodes + 1):
                dp[nodes] += dp[root - 1] * dp[nodes - root]
        return dp[n]
