from typing import *


class Solution:
    def pickGifts(self, gifts: List[int], k: int) -> int:
        import heapq

        gifts = [-g for g in gifts]
        heapq.heapify(gifts)

        for i in range(k):
            max_num = -heapq.heappop(gifts)
            max_num = int(max_num**0.5)
            heapq.heappush(gifts, -max_num)
            # print(gifts)

        return sum(-g for g in gifts)


if __name__ == "__main__":
    gifts = [25, 64, 9, 4, 100]
    k = 4
    gifts = [1, 1, 1, 1]
    k = 4
    result = Solution().pickGifts(gifts, k)
    print(result)
