from typing import *


class Solution:
    def longestSubsequenceRepeatedK(self, s: str, k: int) -> str:
        n = len(s)
        counts = [0 for _ in range(26)]
        # print(counts)
        for i in range(n):
            counts[ord(s[i]) - ord("a")] += 1
        # print(counts)
        letters = []
        for i in range(26):
            while counts[i] >= k:
                letters.append(chr(i + ord("a")))
                counts[i] -= k
        letters.sort()
        # print(letters)

        # 使用DFS寻找最长且字典序最大的子序列
        result = [""]  # 存储当前找到的最优子序列，初始为空字符串

        def isSubsequence(subseq: str, s: str) -> bool:
            """检查 subseq 是否是 s 的子序列"""
            it = iter(s)  # 创建字符串s的迭代器
            return all(
                c in it for c in subseq
            )  # 检查subseq的每个字符是否按顺序出现在s中

        def dfs(current: str, remaining: list):
            # 检查 current * k 是否是 s 的子序列
            if isSubsequence(current * k, s):
                # 如果current长度大于已知最优，或长度相同但字典序更大，则更新结果
                if len(current) > len(result[0]) or (
                    len(current) == len(result[0]) and current > result[0]
                ):
                    result[0] = current  # 更新最优解

                # 从后往前尝试添加字母（保证字典序最大）
                for i in range(len(remaining) - 1, -1, -1):
                    char = remaining[i]  # 取出当前字母
                    new_remaining = (
                        remaining[:i] + remaining[i + 1 :]
                    )  # 移除已选字母后的剩余列表
                    dfs(current + char, new_remaining)

        dfs("", letters)  # 从空字符串和全部字母开始DFS
        return result[0]  # 返回找到的最优子序列


if __name__ == "__main__":
    s = "letsleetcode"
    k = 2
    result = Solution().longestSubsequenceRepeatedK(s, k)
    print(result)
