from typing import *
class Solution:
    def longestSubsequence(self, s: str, k: int) -> int:
        length=len(s)
        index=length-1
        left=k
        while 1:
            # print(left)
            if s[index]=="1":
                left-= 2**(length-1-index)
            if index==0:
                if left>=0:
                    return length
                else :return length-1
            if left<0:
                break
            index -=1

        res=length-1-index
        while index >=0:
            if s[index]=="0":
                res+=1
            index-=1
        return res



if __name__ == "__main__":
    s = "00101001"
    k = 1
    result = Solution().longestSubsequence(s, k)
    print(result)
