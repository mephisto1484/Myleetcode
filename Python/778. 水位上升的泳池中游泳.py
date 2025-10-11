from typing import *


class Solution:
    def swimInWater(self, grid: List[List[int]]) -> int:
        n = len(grid)
        if n == 1:
            return 0
        upper = n * n
        lower = 0
        # print(upper)

        def ok(h):
            if h < grid[0][0]:
                return False
            area = [[False] * n for _ in range(n)]
            area[0][0] = True
            stack = [(0, 0)]
            visited = [[False] * n for _ in range(n)]
            while stack:
                # print(stack)
                x, y = stack.pop()
                if visited[x][y]:
                    continue
                for dx, dy in [[0, 1], [0, -1], [1, 0], [-1, 0]]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < n and 0 <= ny < n and grid[nx][ny] <= h:
                        if visited[nx][ny]:
                            continue
                        area[nx][ny] = True
                        stack.append((nx, ny))
                    elif 0 <= nx < n and 0 <= ny < n:
                        visited[nx][ny] = True
                visited[x][y] = True
            # print(h, area, area[n - 1][n - 1])
            return area[n - 1][n - 1]

        # print(ok(upper))
        while upper - lower > 1:
            mid = (upper + lower) // 2
            if ok(mid):
                upper = mid
            else:
                lower = mid
        return upper


if __name__ == "__main__":
    grid = [[0, 2], [1, 3]]
    grid = [
        [0, 1, 2, 3, 4],
        [24, 23, 22, 21, 5],
        [12, 13, 14, 15, 16],
        [11, 17, 18, 19, 20],
        [10, 9, 8, 7, 6],
    ]
    grid = [[3, 2], [0, 1]]
    grid = [
        [7, 23, 21, 9, 5],
        [3, 20, 8, 18, 15],
        [14, 13, 1, 0, 22],
        [2, 10, 24, 17, 12],
        [6, 16, 19, 4, 11],
    ]
    result = Solution().swimInWater(grid)
    print(result)
