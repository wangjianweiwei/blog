# -*- coding: utf-8 -*-
"""
@Author: 王剑威
@Time: 2020/10/31 8:59 上午
"""
from typing import Dict

"""
LRU算法就是一种缓存淘汰策略, 需要对数据结构进行层层抽象和拆解

计算机的缓存容量有限, 如果缓存满了就要删除一些内容, 给新内容腾出位置, 但问题是, 删除那些内容呢?
我们肯定希望删除那些没有什么用的缓存数据, 而把有用的数据继续保留在缓存里, 方便之后继续使用.
那么, 什么样的数据被判定为`有用的数据`

LRU缓存淘汰策略就是常用的策略.
LRU的全称是Least Recently Used, 也就是说, 我们认为最近使用过的数据应该是`有用的`, 很久都没用过的应该是个无用的.

一个简单的例子, 手机的后台管理.

LRU 缓存算法的核心数据结构就是哈希链表
哈希表查找快，但是数据无固定顺序；链表有顺序之分，插入删除快，但是查找慢。所以结合一下，形成一种新的数据结构：哈希链表 LinkedHashMap。
"""


class Node:
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.next: Node = None
        self.prev: Node = None

    def __repr__(self):
        return f"({self.key}, {self.val})"


class DoubleList:
    def __init__(self):
        self.head: Node = Node(0, 0)
        self.tail: Node = Node(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head
        self.size: int = 0

    def __str__(self):
        curr = self.tail.prev
        res = []
        while curr.prev:
            res.append(curr)
            curr = curr.prev

        return str(res)

    def append(self, node: Node):
        node.prev = self.tail.prev
        node.next = self.tail
        self.tail.prev.next = node
        self.tail.prev = node
        self.size += 1

    def remove(self, node: Node):
        node.prev.next = node.next
        node.next.prev = node.prev
        self.size -= 1

    def remove_first(self):
        if self.head.next == self.tail:
            return

        node = self.head.next
        self.remove(node)

        return node


class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.map: Dict[int, Node] = dict()
        self.cache = DoubleList()

    def make_recently(self, key: int):
        """
        将某个元素提升为最近使用的

        :param key:
        :return:
        """
        node = self.map.get(key)
        # 先从链表中删除这个节点
        self.cache.remove(node)
        # 重新插到队尾
        self.cache.append(node)

        return node

    def add_recently(self, key: int, val):
        """
        添加最近使用的元素

        :param key:
        :param val:
        :return:
        """
        node = Node(key=key, val=val)
        # 链表尾部就是最近使用的元素
        self.cache.append(node)
        # 别忘了在 map 中添加 key 的映射
        self.map[key] = node

        return node

    def delete_key(self, key: int):
        """
        删除某一个元素

        :param key:
        :return:
        """
        node = self.map.get(key)
        # 从链表中删除
        self.cache.remove(node)
        # 从 map 中删除
        self.map.pop(key)

        return node

    def remove_least_recently(self):
        """
        删除最久未使用的元素

        :return:
        """
        # 链表头部的第一个元素就是最久未使用的
        node = self.cache.remove_first()
        # 同时别忘了从 map 中删除它的 key
        if node:
            self.map.pop(node.key)

        return node

    def get(self, key: int):
        if not self.map.get(key):
            return

        # 将该元素提升为最近使用的
        node = self.make_recently(key)
        return node

    def put(self, key: int, val):
        if node := self.get(key):
            node.val = val
        else:
            if self.cache.size >= self.capacity:
                self.remove_least_recently()

            node = self.add_recently(key=key, val=val)

        return node


if __name__ == '__main__':
    cache = LRUCache(capacity=5)
    cache.put(10, 20)
    cache.put(11, 21)
    cache.put(12, 22)
    cache.put(13, 23)
    cache.put(14, 24)
    print(cache.cache)
    print(cache.get(11))
    print(cache.cache)
    cache.delete_key(11)
    print(cache.cache)
    print(cache.get(10))
    print(cache.cache)
    cache.put(15, 25)
    print(cache.cache)
    cache.put(16, 26)
    print(cache.cache)
