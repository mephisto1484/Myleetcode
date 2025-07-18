from typing import *

class Solution:
    def validSubstringCount(self, word1: str, word2: str) -> int:
        # 使用列表代替字典，索引为字母的ASCII值减去'a'的ASCII值
        map2 = [0] * 26
        mem = [0] * 26
        
        # 初始化map2
        for val in word2:
            idx = ord(val) - ord('a')
            map2[idx] += 1
        
        match, len1, len2 = 0, len(word1), len(word2)
        if len1 < len2: 
            return 0
        
        # 用于存储可行的结束位置 end是可达的
        end_location = []
        begin, end = 0, -1
        
        # 初始化窗口
        for i, val in enumerate(word1):
            idx = ord(val) - ord('a')
            if map2[idx] > 0:
                mem[idx] += 1
                if mem[idx] <= map2[idx]:
                    match += 1
            if match == len2:
                end = i
                break
        
        if match != len2: 
            return 0
        end_location.append(end)
        
        while True:
            # 移动左指针
            begin_idx = ord(word1[begin]) - ord('a')
            if map2[begin_idx] > 0:
                mem[begin_idx] -= 1
                if mem[begin_idx] < map2[begin_idx]:
                    # 失去匹配，移动右边
                    end += 1
                    while end < len1:
                        end_idx = ord(word1[end]) - ord('a')
                        if map2[end_idx] > 0:
                            mem[end_idx] += 1
                            if word1[end] == word1[begin]:
                                end_location.append(end)
                                begin += 1
                                break
                            else:
                                end += 1
                        else:
                            end += 1
                    if end == len1:
                        break
                else:
                    begin += 1
                    end_location.append(end)
            else:
                begin += 1
                end_location.append(end)
        
        return len(end_location) * len1 - sum(end_location)


if __name__ == "__main__":
    word1 = "abcabc"
    word2 = "abc"
    result = Solution().validSubstringCount(word1, word2)
    print(result)