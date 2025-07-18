from typing import *


class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        str1, str2 = text1, text2
        area = [[0 for _ in range(len(str1) + 1)] for _ in range(len(str2) + 1)]
        max_ = 0
        len1, len2 = len(str1), len(str2)
        for i in range(1, len2 + 1):
            for j in range(1, len1 + 1):
                area[i][j] = max(
                    area[i - 1][j - 1] + (str1[j - 1] == str2[i - 1]),
                    max(area[i - 1][j], area[i][j - 1]),
                )

        return area[len2][len1]


if __name__ == "__main__":
    text1 = "abcde"
    text2 = "ace"
    result = Solution().longestCommonSubsequence(text1, text2)
    print(result)
