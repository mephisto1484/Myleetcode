from typing import *
class Solution:
    def maximalRectangle(self, matrix: List[str]) -> int:
        if len(matrix) == 0 :
            return 0
        x_len,y_len=len(matrix),len(matrix[0])

        
        # 初始化为matrix[0]每个点的深度
        deepth=[]
        for i in range(0,x_len):
            for j in range(0,y_len):
                if matrix[i][j] == "0":
                    deepth.append(j)
                    break
                elif j==y_len-1:
                    deepth.append(j+1)   

        # print(deepth)
        # 计算当前矩形图
        def largestRectangleArea(heights: List[int]) -> int:
            # right[i]在右侧可以到达的最大位置（不含）,left左侧可到达最大位置（不含）
            right,left=[],[]
            length=len(heights)
            for i in range(length):
                right.append(0)
                left.append(0)
            stack=[]
            stack.append(0)
            for i in range(1,length):
                while len(stack)>0 and heights[i]<heights[stack[-1]]:
                    right[stack[-1]]=i
                    stack.pop()
                stack.append(i)
            while len(stack)>0:
                right[stack[-1]]=length
                stack.pop()

            stack.append(length-1)
            for i in range(1,length):
                j=length-i-1
                while len(stack)>0 and heights[j]<heights[stack[-1]]:
                    left[stack[-1]]=j
                    stack.pop()
                stack.append(j)
            while len(stack)>0:
                left[stack[-1]]=-1
                stack.pop()

            ans=0
            for i in range(length):
                tmp=heights[i]*(right[i]-left[i]-1)
                ans = tmp if tmp > ans else  ans
            return ans

        res=largestRectangleArea(deepth)

        # 对每行，更新matrix并计算res
        for i in range(1,y_len):
            for j in range(0,x_len):
                if matrix[j][i] == "0":
                    deepth[j] = 0
                elif matrix[j][i-1] =="1":
                    deepth[j] -=1
                else :
                    for k in range(i,y_len):
                        if matrix[j][k] =="0":
                            deepth[j]=k-i
                            break
                        if k==y_len-1:
                            deepth[j]=y_len-i
            # print(deepth)
            res_this_line=largestRectangleArea(deepth)
            res = res_this_line if res_this_line>res else res
        
        return res

    


if __name__ == "__main__":
    matrix = ["00"]
    result = Solution().maximalRectangle(matrix)
    print(result)
