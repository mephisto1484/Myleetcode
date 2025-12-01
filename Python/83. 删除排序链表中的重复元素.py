from typing import *


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:

        l0 = ListNode(0)
        result = l0
        while head:
            if head.next and head.val == head.next.val:
                while head.next and head.val == head.next.val:
                    head = head.next
            else:
                l0.next = ListNode(head.val)
                l0 = l0.next
                head = head.next
        return result.next


if __name__ == "__main__":
    # 辅助函数：将列表转换为链表
    def list_to_listnode(lst):
        if not lst:
            return None
        head = ListNode(lst[0])
        current = head
        for val in lst[1:]:
            current.next = ListNode(val)
            current = current.next
        return head

    # 辅助函数：将链表转换为列表（用于打印）
    def listnode_to_list(node):
        result = []
        while node:
            result.append(node.val)
            node = node.next
        return result

    head = [1, 1, 2, 3, 3]
    head = list_to_listnode(head)
    result = Solution().deleteDuplicates(head)
    result = listnode_to_list(result)
    print(result)
