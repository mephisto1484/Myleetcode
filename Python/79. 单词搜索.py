from typing import *


class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        m = len(board)
        n = len(board[0])

        for i in range(m):
            for j in range(n):
                visited = [[False for _ in range(n)] for _ in range(m)]
                if self.dfs(board, word, 0, i, j, visited):
                    return True
        return False

    def dfs(self, board, word, index, startx, starty, visited):
        if index == len(word) - 1:
            return board[startx][starty] == word[index]
        if board[startx][starty] == word[index]:
            visited[startx][starty] = True
            for x, y in [[0, 1], [0, -1], [1, 0], [-1, 0]]:
                newx = startx + x
                newy = starty + y
                if (
                    0 <= newx < len(board)
                    and 0 <= newy < len(board[0])
                    and not visited[newx][newy]
                ):
                    if self.dfs(board, word, index + 1, newx, newy, visited):
                        return True
            visited[startx][starty] = False
            return False
        else:
            return False


if __name__ == "__main__":
    board = [["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]]
    word = "ABCCED"
    board = [["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]]
    word = "SEE"
    board = [["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]]
    word = "ABCB"
    board = [["C", "A", "A"], ["A", "A", "A"], ["B", "C", "D"]]
    word = "AAB"
    board = [["A", "B", "C", "E"], ["S", "F", "E", "S"], ["A", "D", "E", "E"]]
    word = "ABCESEEEFS"
    result = Solution().exist(board, word)
    print(result)
