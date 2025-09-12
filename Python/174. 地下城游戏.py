from typing import *


class Solution:
    def calculateMinimumHP(self, dungeon: List[List[int]]) -> int:
        m = len(dungeon)
        n = len(dungeon[0])
        # print(m, n)
        # return 1

        def isok(num):

            area = [[None for _ in range(n)] for _ in range(m)]
            # print(area)
            area[0][0] = dungeon[0][0] + num
            if area[0][0] <= 0:
                return False
            for i in range(m):
                for j in range(n):
                    if i == 0 and j == 0:
                        pass
                    elif i == 0 and area[i][j - 1]:
                        area[i][j] = area[i][j - 1] + dungeon[i][j]
                    elif j == 0 and area[i - 1][j]:
                        area[i][j] = area[i - 1][j] + dungeon[i][j]
                    else:
                        if area[i][j - 1] and area[i - 1][j]:
                            area[i][j] = max(
                                area[i][j - 1] + dungeon[i][j],
                                area[i - 1][j] + dungeon[i][j],
                            )
                        elif area[i][j - 1]:
                            area[i][j] = area[i][j - 1] + dungeon[i][j]
                        elif area[i - 1][j]:
                            area[i][j] = area[i - 1][j] + dungeon[i][j]
                        else:
                            pass
                    if area[i][j] is not None and area[i][j] <= 0:
                        area[i][j] = None
            # print(area)
            return area[m - 1][n - 1] is not None

        up = 400 * 1000 + 100
        down = 0
        while up - down > 1:
            mid = (up + down) // 2
            if isok(mid):
                up = mid
            else:
                down = mid
        return up


if __name__ == "__main__":
    dungeon = [[-2, -3, 3], [-5, -10, 1], [10, 30, -5]]
    result = Solution().calculateMinimumHP(dungeon)
    print(result)
