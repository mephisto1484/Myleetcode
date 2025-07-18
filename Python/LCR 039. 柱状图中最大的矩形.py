from typing import *


class Solution:
    def largestRectangleArea(self, heights: List[int]) -> int:
        # right[i]在右侧可以到达的最大位置（不含）,left左侧可到达最大位置（不含）
        right, left = [], []
        length = len(heights)
        for i in range(length):
            right.append(0)
            left.append(0)
        stack = []
        stack.append(0)
        for i in range(1, length):
            while len(stack) > 0 and heights[i] < heights[stack[-1]]:
                right[stack[-1]] = i
                stack.pop()
            stack.append(i)
        while len(stack) > 0:
            right[stack[-1]] = length
            stack.pop()

        stack.append(length - 1)
        for i in range(1, length):
            j = length - i - 1
            while len(stack) > 0 and heights[j] < heights[stack[-1]]:
                left[stack[-1]] = j
                stack.pop()
            stack.append(j)
        while len(stack) > 0:
            left[stack[-1]] = -1
            stack.pop()

        ans = 0
        for i in range(length):
            tmp = heights[i] * (right[i] - left[i] - 1)
            ans = tmp if tmp > ans else ans
        return ans


if __name__ == "__main__":
    heights = [2, 4]
    result = Solution().largestRectangleArea(heights)
    print(result)
