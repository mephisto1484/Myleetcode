from typing import *


class Solution:
    def replaceNonCoprimes(self, nums: List[int]) -> List[int]:
        cache = {}

        def gcd(a: int, b: int) -> int:
            # 统一让 a >= b，减少递归深度
            if a < b:
                a, b = b, a
            if b == 0:
                return a
            if (a, b) in cache:
                return cache[(a, b)]
            g = gcd(b, a % b)  # 递归
            cache[(a, b)] = g
            return g

        st = []
        for x in nums:
            st.append(x)
            # 只要栈顶两个不互质就合并
            while len(st) >= 2:
                a, b = st[-2], st[-1]
                g = gcd(a, b)
                if g == 1:
                    break
                st.pop()
                st.pop()
                st.append(a // g * b)  # 合并后值
        return st


if __name__ == "__main__":
    nums = [6, 4, 3, 2, 7, 6, 2]
    nums = [11, 9, 3, 9, 3, 9, 33]
    result = Solution().replaceNonCoprimes(nums)
    print(result)
