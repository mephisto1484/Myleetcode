from typing import *
class Solution:
    def longestSubsequenceRepeatedK(self, s: str, k: int) -> str:
        def canMatch(s, sub, k):
            count = 0
            i = 0
            n = len(s)
            m = len(sub)
            while count < k and i <= n - m:
                pos = 0
                j = i
                while j < n and pos < m:
                    if s[j] == sub[pos]:
                        pos += 1
                    j += 1
                if pos == m:
                    count += 1
                    i = j
                else:
                    break
            return count >= k

        freq = [0] * 26
        for c in s:
            freq[ord(c) - ord('a')] += 1
        
        # Collect characters with frequency >= k, sorted by frequency descending and then char descending
        chars = []
        for i in range(25, -1, -1):
            if freq[i] >= k:
                chars.append((freq[i], chr(i + ord('a'))))
        chars.sort(reverse=True)
        chars = [c for (f, c) in chars]
        
        if not chars:
            return ""
        
        max_len = min(len(s) // k, sum(f // k for f in freq))
        for L in range(max_len, 0, -1):
            # Generate candidates by taking the most frequent characters first
            # Try to maximize the number of high-frequency characters in the candidate
            # Here, we try all possible combinations of characters with their maximum possible counts
            from itertools import product
            max_counts = [freq[ord(c) - ord('a')] // k for c in chars]
            # Generate all possible counts for each character that sum to L
            # This is a bit involved, so we use a heuristic: try to assign as many as possible to the highest frequency character
            # For simplicity, we can try to assign the maximum possible to the first character, then the next, etc.
            candidate = []
            remaining = L
            for c in chars:
                take = min(max_counts[chars.index(c)], remaining)
                candidate.extend([c] * take)
                remaining -= take
                if remaining == 0:
                    break
            candidate = ''.join(candidate)
            if canMatch(s, candidate, k):
                return candidate
            
            # If the heuristic fails, try all unique combinations
            # This is expensive, but ensures correctness
            from itertools import combinations_with_replacement
            seen = set()
            for c in combinations_with_replacement(chars, L):
                candidate = ''.join(sorted(c, reverse=True))
                if candidate not in seen:
                    seen.add(candidate)
                    if canMatch(s, candidate, k):
                        return candidate
        return ""

        


if __name__ == "__main__":
    s = "letsleetcode"
    k = 2
    result = Solution().longestSubsequenceRepeatedK(s,k)
    print(result)
