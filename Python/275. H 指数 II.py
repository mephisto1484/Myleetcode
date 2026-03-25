from typing import *


class Solution:
    def hIndex(self, citations: List[int]) -> int:
        begin= min (len(citations),1000)
        if citations[len(citations)-begin]>=begin:
            return begin
        left,right=0,begin

        while right-left>1:
            middle=(left+right)//2
            if citations[len(citations)-middle]>=middle:
                left=middle
            else:
                right=middle
        return left





        pass


if __name__ == "__main__":
    citations = [0,1,3,5,6]
    citations = [1,2,100]
    result = Solution().hIndex(citations)
    print(result)
