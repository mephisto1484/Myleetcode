from typing import *

class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        s_len, p_len = len(s), len(p)
        # 使用字典作为缓存，键是 (s_index, p_index)，值是布尔值
        cache = {}

        def match(s_index: int, p_index: int) -> bool:
            # 如果结果已经在缓存中，直接返回
            if (s_index, p_index) in cache:
                return cache[(s_index, p_index)]

            # 如果 p 和 s 都匹配完了，返回 True
            if s_index == s_len and p_index == p_len:
                return True
            # 如果 p 到了末尾，而 s 还没有匹配完，返回 False
            if p_index == p_len:
                return False

            # 当前字符是否匹配
            first_match = s_index < s_len and (s[s_index] == p[p_index] or p[p_index] == '.')

            # 如果下一个字符是 '*'
            if p_index + 1 < p_len and p[p_index + 1] == '*':
                # 两种情况：
                # 1. 跳过 "x*"（即匹配零次）
                # 2. 保留 "x*"，并尝试匹配一个字符（如果当前字符匹配）
                result = match(s_index, p_index + 2) or (first_match and match(s_index + 1, p_index))
            else:
                # 如果下一个字符不是 '*'
                result = first_match and match(s_index + 1, p_index + 1)

            # 将结果存入缓存
            cache[(s_index, p_index)] = result
            return result

        return match(0, 0)

if __name__ == "__main__":
    s = "aab"
    p = "c*a*b"
    result = Solution().isMatch(s, p)
    print(result)
