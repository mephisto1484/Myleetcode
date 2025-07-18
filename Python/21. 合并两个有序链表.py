from typing import *

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        head=ListNode(0)
        index=head

        while list1 and list2:
            min_=min(list1.val,list2.val)
            if list1.val<list2.val:
                list1=list1.next
            else:
                list2=list2.next
            
            index.next=ListNode(min_)
            index=index.next

        if list1:
            index.next=list1
        elif list2:
            index.next=list2

        return head.next



if __name__ == "__main__":
    pass
    # l1 = [1,2,4]
    # l2 = [1,3,4]
    # result = Solution.mergeTwoLists(l1, l2)
    # print(result)
