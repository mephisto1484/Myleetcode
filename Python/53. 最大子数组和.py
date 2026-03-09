from typing import *


class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        sums= [0 for _ in nums]
        for i in range(len(nums)):
            sums[i] = max(sums[i-1]+nums[i], nums[i]) 
        return max(sums)



if __name__ == "__main__":
    nums = [-2,1,-3,4,-1,2,1,-5,4]
    nums = [1]
    nums = [5,4,-1,7,8]
    result = Solution().maxSubArray(nums)
    print(result)
