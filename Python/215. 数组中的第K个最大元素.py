from typing import *


class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        # 第 k 大等价于第 (n - k + 1) 小
        n = len(nums)
        return self._select(nums, 0, n - 1, n - k + 1)

    def _select(self, A: List[int], l: int, r: int, k: int) -> int:
        """在 A[l..r] 中找第 k 小（k 从 1 开始）"""
        if r - l + 1 <= 5:
            A[l:r + 1] = sorted(A[l:r + 1])
            return A[l + k - 1]

        # 1. 每 5 个一组，组内排序，取中位数移到数组前部
        m = 0
        i = l
        while i <= r:
            j = min(i + 4, r)
            A[i:j + 1] = sorted(A[i:j + 1])
            mid = (i + j) // 2
            A[l + m], A[mid] = A[mid], A[l + m]
            m += 1
            i += 5

        # 2. 递归找“中位数的中位数”作为 pivot
        pivot = self._select(A, l, l + m - 1, (m + 1) // 2)

        # 3. 三路划分
        lt, gt = self._partition3(A, l, r, pivot)

        leftSize = lt - l          # 小于 pivot 的元素个数
        equalEnd = gt - l + 1      # 小于等于 pivot 的元素个数

        if k <= leftSize:
            return self._select(A, l, lt - 1, k)
        elif k <= equalEnd:
            return pivot
        else:
            return self._select(A, gt + 1, r, k - equalEnd)

    def _partition3(self, A: List[int], l: int, r: int, pivot: int) -> Tuple[int, int]:
        """三路划分：小于 pivot、等于 pivot、大于 pivot"""
        lt = l
        i = l
        gt = r
        while i <= gt:
            if A[i] < pivot:
                A[lt], A[i] = A[i], A[lt]
                lt += 1
                i += 1
            elif A[i] > pivot:
                A[i], A[gt] = A[gt], A[i]
                gt -= 1
            else:
                i += 1
        return lt, gt


if __name__ == "__main__":
    solution = Solution()
    print(solution.findKthLargest([3, 2, 1, 5, 6, 4], 2))            # 5
    print(solution.findKthLargest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4))  # 4
    print(solution.findKthLargest([1], 1))                          # 1
    print(solution.findKthLargest([3, 3, 3, 3], 2))                 # 3
    print(solution.findKthLargest([-1, -2, -3, -4], 2))             # -2
    print(solution.findKthLargest([5, 2, 8, 1, 9], 5))              # 1
    print(solution.findKthLargest([7, 6, 5, 4, 3, 2, 1], 3))        # 5
    print(solution.findKthLargest([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 1))   # 10
    print(solution.findKthLargest([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 10))  # 1