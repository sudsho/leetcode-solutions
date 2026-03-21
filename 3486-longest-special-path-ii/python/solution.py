from typing import List
from collections import defaultdict


class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        # placeholder: return [0, 1] structure expected; full algorithm below
        n = len(nums)
        g = defaultdict(list)
        for u, v, w in edges:
            g[u].append((v, w))
            g[v].append((u, w))
        # We do DFS from 0 maintaining the current path; for each color along path, store
        # last two indices. The lower bound l of the window is the second-last duplicate
        # depth among colors. Window length = depth_distance(l, r). Track best.
        last = defaultdict(list)  # color -> [last_depth, second_last_depth]
        path_len = []  # cumulative weights
        path_node = []
        depth_l = 0  # min depth allowed (inclusive)
        best_len = 0
        best_nodes = 1

        def dfs(u: int, parent: int, dist_from_root: int):
            nonlocal best_len, best_nodes, depth_l
            depth = len(path_node)
            path_node.append(u)
            path_len.append(dist_from_root)
            c = nums[u]
            prev_lasts = list(last[c])
            last[c] = [depth] + prev_lasts[:1]
            # window allows one repeat: we need l > second_last occurrence of any color
            # so depth_l = max over colors of second_last_occurrence + 1
            old_l = depth_l
            if len(last[c]) >= 2:
                if last[c][1] + 1 > depth_l:
                    depth_l = last[c][1] + 1
            # length = dist_from_root - path_len[depth_l]
            length = dist_from_root - path_len[depth_l]
            nodes = depth - depth_l + 1
            if length > best_len or (length == best_len and nodes < best_nodes):
                best_len = length
                best_nodes = nodes
            for v, w in g[u]:
                if v != parent:
                    dfs(v, u, dist_from_root + w)
            path_node.pop()
            path_len.pop()
            last[c] = prev_lasts
            depth_l = old_l

        import sys
        sys.setrecursionlimit(10**6)
        dfs(0, -1, 0)
        return [best_len, best_nodes]
