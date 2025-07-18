from typing import *


class Solution:
    def minWindow(self, s: str, t: str) -> str:
        # s 母串  t目标串
        s_len, t_len = len(s), len(t)
        # weight t中字母都出现几次
        weight = {}
        for i, val in enumerate(t):
            if weight.get(val):
                weight[val] += 1
            else:
                weight[val] = 1
        # print(weight)
        # mem 记录已经找到了多少个t中字母
        mem = {}
        for i, val in enumerate(weight):
            mem[val] = 0

        # 找第一次覆盖 begin记录左位置，end记录右位置
        begin, end, matchsize = -1, -1, 0
        for i, val in enumerate(s):
            if weight.get(val):
                begin = i if begin < 0 else begin
                mem[val] += 1
                if mem[val] <= weight[val]:
                    matchsize += 1
                if matchsize == t_len:
                    end = i
                    break
        if end == -1:
            return ""
        # print(begin,end,s[begin:end+1])

        # 压缩左侧，可能有重复的，直至不能再压缩
        # 此时得到以end为右侧的 最小覆盖
        def left_move(begin, end):
            while 1:
                if weight.get(s[begin]):
                    if weight[s[begin]] == mem[s[begin]]:
                        break
                    else:
                        mem[s[begin]] -= 1
                        begin += 1
                else:
                    begin += 1
            # print(begin,end,s[begin:end+1])
            return begin, end

        x, y = left_move(begin, end)
        min_, min_x, min_y = y - x, x, y

        # 移动右侧，每达到下一次覆盖时，重新压缩左侧
        for i in range(end + 1, s_len):
            # 遇到在串中的，记下来
            if weight.get(s[i]):
                mem[s[i]] += 1
            if s[x] == s[i]:
                # 左侧可以移动了
                x, y = left_move(x, i)
                if min_ > y - x:
                    min_, min_x, min_y = y - x, x, y

        return s[min_x : min_y + 1]


if __name__ == "__main__":
    s = "cabwefgewcwaefgcf"
    t = "cae"
    result = Solution().minWindow(s, t)
    print(result)
