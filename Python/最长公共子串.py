from typing import *
class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        s1=text1
        s2=text2
        len_1=len(s1)
        len_2=len(s2)

        area=[ [0 for _ in range(len_1+1)] for _ in range (len_2+1)]
        max_=0

        for i in range(1,len_2+1):
            for j in range(1,len_1+1):
                # print(i,j)
                if s1[j-1]==s2[i-1]:
                    print(i,j)
                    area[i][j]=area[i-1][j-1]+1
                else:
                    area[i][j]=0
            max_=max(max_,max(area[i]))
            print(area[i])
        # print(area)
        return max_
        
if __name__ == "__main__":
    text1 = "abc"
    text2 = "def"
    result = Solution().longestCommonSubsequence(text1, text2)
    print(result)
