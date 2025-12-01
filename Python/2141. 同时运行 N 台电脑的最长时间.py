from typing import *


class Solution:
    def maxRunTime(self, n: int, batteries: List[int]) -> int:
        def canRunTime(time: int) -> bool:
            """检查是否能运行 time 分钟"""
            total = sum(min(b, time) for b in batteries)
            # min(b, time) 表示：在运行 time 分钟内，这块电池实际能贡献的电量
            return total >= n * time

        # 二分查找最长运行时间
        left, right = 0, sum(batteries) // n

        while left < right:
            mid = (left + right + 1) // 2
            if canRunTime(mid):
                left = mid
            else:
                right = mid - 1

        return left


if __name__ == "__main__":
    n = 2
    batteries = [3, 3, 3]
    # n = 2
    # batteries = [1, 1, 1, 1]
    result = Solution().maxRunTime(n, batteries)
    print(result)
