from typing import *


class Solution:
    def minCost(self, n: int, cost: List[List[int]]) -> int:
        group=[[1,2],[1,3],[2,1],[2,3],[3,1],[3,2]]
        next = [[3,4,5],[3,5,6],[1,2,6],[1,5,6],[1,2,4],[2,3,4]]
        # 1 => 3 4 5
        # 2 => 3 5 6
        # 3 => 1 2 6
        # 4 => 1 5 6
        # 5 => 1 2 4
        # 6 => 2 3 4

        n = n // 2
        area = [[0 for _ in range(6)] for _ in range(n)]

        for i in range(6):
            area[0][i] = cost[n-1][group[i][0]-1]+cost[n][group[i][1]-1]
        # print(area[0])

        for i in range(1, n):
            for j in range(6):
                tmp = cost[n-1-i][group[j][0]-1]+cost[n+i][group[j][1]-1]

                area[i][j] = tmp + min(area[i-1][k-1] for k in next[j])
        # print(area)
        return min(area[n-1])


if __name__ == "__main__":
    n = 4
    cost = [[3,5,7],[6,2,9],[4,8,1],[7,3,5]]
    n = 6
    cost = [[2,4,6],[5,3,8],[7,1,9],[4,6,2],[3,5,7],[8,2,4]]
    result = Solution().minCost(n, cost)
    print(result)
