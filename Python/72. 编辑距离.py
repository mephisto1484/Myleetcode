from typing import *
# 代码中已指定的类名、方法名、参数名，请勿修改，直接返回方法规定的值即可

class Solution :
    def minDistance(self, word1: str, word2: str) -> int:
        #write your code here.
        area = [[0 for _ in range(len(word1) + 1) ]  for _ in range(len(word2) + 1)]
        len_1,len_2= len(word1),len(word2)
        if len_1==0 or len_2==0:
          return len_1+len_2
          
        for i in range(len_2+1):
          area[i][0] = i
        for j in range(len_1+1):
          area[0][j] = j
        
        # print(area)
        
        for i in range(1,len_2+1):
          for j in range(1,len_1+1):
            if word2[i-1]==word1[j-1]:
              area[i][j]=area[i-1][j-1]
            else:
              area[i][j]= min(min(area[i][j-1],area[i-1][j-1]),area[i-1][j])+1
              
        # print(area)
        return area[len_2][len_1]
        
if __name__ == "__main__":
    word1 = "horse"
    word2 = "ros"
    result = Solution().minDistance(word1,word2)
    print(result)