from typing import *


class Solution:
    def sortByBits(self, arr: List[int]) -> List[int]:
        bit_nums = [2**i for i in range(14)]
        bit_nums.reverse()
        groups = [[] for _ in range(14)]
        # print(bit_nums)

        for num in arr:
            now_num = num
            j = 0
            for i, bit_num in enumerate(bit_nums):

                if now_num >= bit_num:
                    j+= 1
                    now_num -= bit_num
                else:
                    pass
            groups[j].append(num)

        for group in groups:
            # print(group)
            group.sort()
        result = []
        for group in groups:
            result.extend(group)
        # print(result)
        return result


        pass


if __name__ == "__main__":
    arr = [0,1,2,3,4,5,6,7,8]
    arr = [1024,512,256,128,64,32,16,8,4,2,1]
    arr = [10000,10000]
    arr =[2,3,5,7,11,13,17,19]
    arr = [10,100,1000,10000]
    # target = 9
    result = Solution().sortByBits(arr)
    print(result)
