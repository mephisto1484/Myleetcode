from typing import *
# Definition for singly-linked list.

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        result=ListNode(0)
        now=result
        plus=0

        while l1 or l2 or plus:
            tmp= (l1.val if l1 else 0) +  (l2.val if l1 else 0) + plus
            if tmp >= 10:
                tmp -= 10
                plus =1
            else:
                plus=0
            now.val=tmp
            now=now.next
            l1 = l1.next if l1 else None
            l2 = l2.next if l1 else None
        print(result.next)
        return result.next

if __name__ == "__main__":
    l1 = [2,4,3], l2 = [5,6,4]
    result=Solution().addTwoNumbers(l1,l2)

    print(result)