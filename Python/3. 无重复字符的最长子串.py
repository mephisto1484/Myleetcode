from typing import *
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        lib=set()
        str_len=len(s)
        begin=0
        max_num =0

        for i in range (str_len):
            if s[i] not in lib:
                lib.add(s[i])
            else:
                max_num=len(lib) if len(lib) >  max_num else max_num
                while s[begin]!=s[i]:
                    if s[begin] in lib:
                        lib.remove(s[begin])
                    begin+=1
                begin +=1
            # print(i,s[i],begin,s[begin],lib)
        max_num=len(lib) if len(lib) >  max_num else max_num
        return max_num


if __name__ == "__main__":
    s = "a"
    result = Solution().lengthOfLongestSubstring(s)
    print(result)
