from typing import *


class Solution:
    def minOperations(self, queries: List[List[int]]) -> int:
        def sum_div4_times(a: int, b: int) -> int:
            """∑_{i=a}^{b} 把 i 不断//4 直到 0 所需的次数"""
            if a > b:
                return 0
            total = 0
            k = 0
            while True:
                L = 4**k
                R = 4 ** (k + 1)
                segL = max(a, L)
                segR = min(b, R - 1)
                if segL <= segR:
                    total += (k + 1) * (segR - segL + 1)
                if R > b:
                    break
                k += 1
            return total

        res = 0
        for l, r in queries:
            res += (sum_div4_times(l, r) + 1) // 2
        return res


if __name__ == "__main__":
    queries = [[1, 2], [2, 4]]
    result = Solution().minOperations(queries)
    print(result)
