from typing import *


class Solution:
    def singleNonDuplicate(self, nums: List[int]) -> int:
        left = 0
        right = len(nums)
        if right == 1:
            return nums[0]
        while 1:
            mid = (left + right) // 2
            print(left, mid, right)
            if right - left == 1:
                return nums[left]
            if right - left == 3:
                return (
                    nums[left] if nums[left + 1] == nums[left + 2] else nums[left + 2]
                )

            location = mid - 1 if nums[mid] == nums[mid - 1] else mid
            if location % 2 == 0:
                # 在后半段 从location到right
                left = location
            else:
                # 在左半段 从left到location
                right = location


if __name__ == "__main__":
    nums = [1, 1, 2, 3, 3, 4, 4, 8, 8]
    result = Solution().singleNonDuplicate(nums)
    print(result)
