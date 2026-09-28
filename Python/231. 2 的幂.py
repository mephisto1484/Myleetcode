from typing import *


class Solution:
    def isPowerOfTwo(self, n: int) -> bool:
        # print(n&(n-1))
        return n>0 and (not (bool(n&(n-1))))


if __name__ == "__main__":
    solution = Solution()
    print(solution.isPowerOfTwo(1))  # True
    print(solution.isPowerOfTwo(16))  # True
    print(solution.isPowerOfTwo(3))  # False


