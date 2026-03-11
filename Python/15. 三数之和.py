from typing import *


class Solution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        nums.sort()
        results: list[list[int]] = []
        n = len(nums)

        for i in range(n - 2):
            if i > 0 and nums[i] == nums[i - 1]:
                continue

            if nums[i] > 0:
                break

            target = -nums[i]
            left, right = i + 1, n - 1

            while left < right:
                s = nums[left] + nums[right]
                if s == target:
                    results.append([nums[i], nums[left], nums[right]])
                    left += 1
                    while left < right and nums[left] == nums[left - 1]:
                        left += 1
                    right -= 1
                    while left < right and nums[right] == nums[right + 1]:
                        right -= 1
                elif s < target:
                    left += 1
                else:
                    right -= 1

        return results




if __name__ == "__main__":
    nums = [-1,0,1,2,-1,-4]
    nums = [0,0,0]
    result = Solution().threeSum(nums)
    print(result)
