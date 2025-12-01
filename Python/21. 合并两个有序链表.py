from typing import *


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def mergeTwoLists(
        self, list1: Optional[ListNode], list2: Optional[ListNode]
    ) -> Optional[ListNode]:
        head = ListNode(0)
        index = head

        while list1 and list2:
            min_ = min(list1.val, list2.val)
            if list1.val < list2.val:
                list1 = list1.next
            else:
                list2 = list2.next

            index.next = ListNode(min_)
            index = index.next

        if list1:
            index.next = list1
        elif list2:
            index.next = list2

        return head.next


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

    l1 = [1, 2, 4]
    l2 = [1, 3, 4]

    # 创建 Solution 实例，并转换输入
    list1 = list_to_listnode(l1)
    list2 = list_to_listnode(l2)
    result = Solution().mergeTwoLists(list1, list2)

    # 打印结果
    print(listnode_to_list(result))  # 输出: [1, 1, 2, 3, 4, 4]
