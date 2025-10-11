from typing import *


class Solution:
    def maximumTotalDamage(self, power: List[int]) -> int:
        weight_set = {}
        for i in range(len(power)):
            if power[i] not in weight_set:
                weight_set[power[i]] = 1
            else:
                weight_set[power[i]] += 1
        # print(weight_set)
        weight = sorted(weight_set.keys())
        nums = [weight_set[k] for k in weight]
        weight.reverse()
        nums.reverse()

        # print(weight)
        # print(nums)
        # print()
        memory = [0] * len(weight)
        memory[0] = weight[0] * nums[0]
        index = 1
        while index < len(weight):
            if weight[index] + 2 < weight[index - 1]:
                last = index - 1
            else:
                if index >= 2:
                    if weight[index] + 2 < weight[index - 2]:
                        last = index - 2
                    else:
                        if index >= 3:
                            last = index - 3
                        else:
                            last = -1
                else:
                    last = -1
            if last == -1:
                memory[index] = max(weight[index] * nums[index], memory[index - 1])
            else:
                memory[index] = max(
                    memory[last] + weight[index] * nums[index], memory[index - 1]
                )
            index += 1
        # print(memory)
        return memory[-1]


if __name__ == "__main__":
    # power = [7, 1, 6, 6]
    power = [5, 9, 2, 10, 2, 7, 10, 9, 3, 8]
    result = Solution().maximumTotalDamage(power)
    print(result)
