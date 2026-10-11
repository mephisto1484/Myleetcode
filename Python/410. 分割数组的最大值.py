from typing import List


class Solution:
    def splitArray(self, nums: List[int], k: int) -> int:
        def can_split(max_sum: int) -> bool:
            count = 1
            cur_sum = 0
            for num in nums:
                if cur_sum + num > max_sum:
                    count += 1
                    cur_sum = num
                    if count > k:
                        return False
                else:
                    cur_sum += num
            return True

        low = max(nums)
        high = sum(nums)
        ans = high

        while low <= high:
            mid = (low + high) // 2
            if can_split(mid):
                ans = mid
                high = mid - 1
            else:
                low = mid + 1

        return ans


if __name__ == "__main__":
    # 示例 1：期望输出 18
    nums1 = [7, 2, 5, 10, 8]
    k1 = 2
    print(Solution().splitArray(nums1, k1))

    # 示例 2：期望输出 9
    nums2 = [1, 2, 3, 4, 5]
    k2 = 2
    print(Solution().splitArray(nums2, k2))

    # 示例 3：只有一组，期望输出总和
    nums3 = [1, 4, 4]
    k3 = 3
    print(Solution().splitArray(nums3, k3))