from typing import *


class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        if not text1 or not text2:
            return 0
        if len(text1) < len(text2):
            text1, text2 = text2, text1
        len1, len2 = len(text1), len(text2)
        prev = [0] * (len2 + 1)
        curr = [0] * (len2 + 1)

        for i in range(1, len1 + 1):
            for j in range(1, len2 + 1):
                if text1[i - 1] == text2[j - 1]:
                    curr[j] = prev[j - 1] + 1
                else:
                    curr[j] = max(prev[j], curr[j - 1])
            prev, curr = curr, prev
            curr = [0] * (len2 + 1)
        return prev[len2]


if __name__ == "__main__":
    text1 = "abcde"
    text2 = "ace"
    result = Solution().longestCommonSubsequence(text1, text2)
    print(result)
