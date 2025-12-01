from typing import *


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        l0 = ListNode(0)
        result = l0.next
        while head:
            if head.next and head.val == head.next.val:
                while head.next and head.val == head.next.val:
                    head = head.next
            else:
                l0.next = ListNode(head.val)
                l0 = l0.next
        pass


if __name__ == "__main__":
    head = [1, 1, 2, 3, 3]
    result = Solution.deleteDuplicates(head)
    print(result)
