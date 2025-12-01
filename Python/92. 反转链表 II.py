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

    def reverseBetween(
        self, head: Optional[ListNode], left: int, right: int
    ) -> Optional[ListNode]:
        # 创建虚拟头节点
        dummy = ListNode(0)
        dummy.next = head
        prev = dummy

        # 找到left位置的前一个节点
        for _ in range(left - 1):
            prev = prev.next

        # left位置的节点
        left_node = prev.next
        # right位置的节点
        right_node = prev.next

        # 找到right位置的节点
        for _ in range(right - left):
            right_node = right_node.next

        # 保存right节点的下一个节点
        next_node = right_node.next

        # 断开right节点和后续节点的连接
        right_node.next = None

        # 反转left到right之间的链表
        reversed_head = self.reverseList(left_node)

        # 连接前面的部分
        prev.next = reversed_head

        # 连接后面的部分（left_node现在是反转后的尾节点）
        left_node.next = next_node

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
    left = 2
    right = 4

    head = [5]
    left = 1
    right = 1

    # 创建 Solution 实例，并转换输入
    head = list_to_listnode(head)

    result = Solution().reverseBetween(head, left, right)

    # 打印结果
    print(listnode_to_list(result))
