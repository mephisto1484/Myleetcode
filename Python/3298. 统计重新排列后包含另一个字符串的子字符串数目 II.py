from typing import *
class Solution:
    def validSubstringCount(self, word1: str, word2: str) -> int:
        map2,mem={},{}
        for i,val in enumerate(word2):
            if map2.get(val): map2[val]+=1
            else : 
                map2[val],mem[val]=1,0
        match,len1,len2=0,len(word1),len(word2)
        if len1<len2 : return 0
        #用于存储可行的结束位置 end是可达的
        end_location=[]
        begin,end=0,-1
        for i,val in enumerate(word1):
            if map2.get(val): 
                mem[val]+=1
                if mem[val]<=map2[val]: match+=1
            if match==len2:
                end=i
                break
        if match!=len2: return 0
        end_location.append(end)
        # print(mem,begin,end)

        while 1:
            # print(mem,begin,end)
            if map2.get(word1[begin]):
                mem[word1[begin]]-=1
                if mem[word1[begin]]<map2[word1[begin]]:
                    # 失去匹配，移动右边
                    end+=1
                    while end<len1:
                        if map2.get(word1[end]):
                            mem[word1[end]]+=1
                            if word1[end]==word1[begin]:
                                end_location.append(end)
                                begin+=1
                                break
                            else: end+=1
                        else:
                            end+=1
                    if end==len1:
                        break
                else: 
                    begin+=1
                    end_location.append(end)
            else:
                begin+=1
                end_location.append(end)
        
        # print(end_location)
        return len(end_location)*len1-sum(end_location)


if __name__ == "__main__":
    word1 = "abcabc"
    word2 = "aaabc"
    result = Solution().validSubstringCount(word1,word2)
    print(result)
