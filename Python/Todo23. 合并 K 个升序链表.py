from typing import *
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        if len(lists)<=1:
            return lists
        import heapq
        q=[]
        for node in lists:
            if node:
                heapq.heappush(q,node)
                
        p=ListNode(0)
        index=p
        while q:
            head=heapq.heappop(q)
            print(head)

        return p.next
  

if __name__ == "__main__":
    lists = [[1,4,5],[1,3,4],[2,6]]
    result = Solution().mergeKLists(lists)
    print(result)
