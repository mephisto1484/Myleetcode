from typing import *


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        dummy = ListNode(0)
        dummy.next = head

        fast = slow = dummy

        # fast 先走 n+1 步
        for _ in range(n + 1):
            fast = fast.next

        # fast 和 slow 一起走，直到 fast 为 None
        while fast:
            fast = fast.next
            slow = slow.next

        # 删除第 n 个节点
        slow.next = slow.next.next

        return dummy.next


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
    n = 2
    # head = [1, 2]
    # n = 1
    # head = [1]
    # n = 1

    # 创建 Solution 实例，并转换输入
    head = list_to_listnode(head)

    result = Solution().removeNthFromEnd(head, n)

    # 打印结果
    print(listnode_to_list(result))  # 输出: [1, 1, 2, 3, 4, 4]
