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

    def reverseKGroup(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        # 检查是否有k个节点
        def checkKNodes(node):
            count = 0
            while node and count < k:
                node = node.next
                count += 1
            return count == k

        # 创建虚拟头节点
        dummy = ListNode(0)
        dummy.next = head
        prev_group = dummy

        while checkKNodes(prev_group.next):
            # 获取当前组的首尾节点
            group_start = prev_group.next
            group_end = prev_group.next

            # 找到当前组的最后一个节点
            for _ in range(k - 1):
                group_end = group_end.next

            # 保存下一组的起始节点
            next_group_start = group_end.next

            # 断开当前组和下一组的连接
            group_end.next = None

            # 反转当前组
            reversed_head = self.reverseList(group_start)

            # 连接前一组和反转后的当前组
            prev_group.next = reversed_head

            # 更新指针：group_start现在是当前组的最后一个节点
            group_start.next = next_group_start
            prev_group = group_start

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
    k = 2
    head = [1, 2, 3, 4, 5]
    k = 3

    # 创建 Solution 实例，并转换输入
    head = list_to_listnode(head)

    result = Solution().reverseKGroup(head, k)

    # 打印结果
    print(listnode_to_list(result))
