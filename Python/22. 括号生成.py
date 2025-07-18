class Solution:
    def generateParenthesis(self, n: int) -> list[str]:
        results = []
        
        def backtrack(current: str, left: int, right: int):
            if left == 0 and right == 0:
                results.append(current)
                return
            if left > 0:
                backtrack(current + "(", left - 1, right)
            if right > left:
                backtrack(current + ")", left, right - 1)
        
        backtrack("", n, n)
        return results

if __name__ == "__main__":
    n = 3
    result=Solution().generateParenthesis(n)

    print(result)