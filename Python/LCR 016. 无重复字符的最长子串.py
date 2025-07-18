from typing import *
# Definition for singly-linked list.


class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        len_s= len(s)
        if len_s==0 or len_s==1:
            return len_s
        mem={}
        max_len,now_len=0,-1
        mem[s[0]]=1
        j=0
        for i in range(1,len_s):
            #print(mem,max_len,s[i])
            # 存在 更新
            if mem.get(s[i]):
                now_len=len(mem)
                max_len=max(now_len,max_len)
                while s[i]!=s[j] and mem.get(s[j]):
                    mem.pop(s[j])
                    j+=1
                j+=1
                

            # 不存在 加入
            else:
                mem[s[i]]=1

        max_len=max(max_len,len(mem))
        return max_len


if __name__ == "__main__":
    #s = "pwwkew"
    s = "abcabcbb"
    result=Solution().lengthOfLongestSubstring(s)

    print(result)