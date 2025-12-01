from typing import *


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        if len(lists) <= 1:
            return lists[0] if lists else None

        import heapq

        q = []
        for i in range(len(lists)):  # 初始化堆
            if lists[i]:
                heapq.heappush(q, (lists[i].val, i))
                lists[i] = lists[i].next

        p = ListNode(0)
        index = p
        while q:
            val, i = heapq.heappop(q)
            index.next = ListNode(val)
            index = index.next
            if lists[i]:
                heapq.heappush(q, (lists[i].val, i))
                lists[i] = lists[i].next
        return p.next


def array_to_linked_list(arr: List[int]) -> Optional[ListNode]:
    """将数组转换为链表"""
    if not arr:
        return None
    head = ListNode(arr[0])
    current = head
    for val in arr[1:]:
        current.next = ListNode(val)
        current = current.next
    return head


def linked_list_to_array(head: Optional[ListNode]) -> List[int]:
    """将链表转换为数组"""
    result = []
    current = head
    while current:
        result.append(current.val)
        current = current.next
    return result


if __name__ == "__main__":
    lists = [[1, 4, 5], [1, 3, 4], [2, 6]]
    lists = []
    lists = [[]]
    # 将数组列表转换为链表列表
    linked_lists = [array_to_linked_list(arr) for arr in lists]
    result = Solution().mergeKLists(linked_lists)
    # 将结果链表转换回数组
    result_array = linked_list_to_array(result)
    print(result_array)
