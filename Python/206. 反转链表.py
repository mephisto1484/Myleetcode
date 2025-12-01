from typing import *


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        mem = ListNode(0)
        p = mem.next
        q = head
        while q:
            tmp = q.next
            q.next = p
            p = q
            q = tmp
        return p


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

    head = [1, 2, 3, 4, 5]
    # k = 2
    # head = [1, 2, 3, 4, 5]
    # k = 3

    # 创建 Solution 实例，并转换输入
    head = list_to_listnode(head)

    result = Solution().reverseList(head)

    # 打印结果
    print(listnode_to_list(result))
