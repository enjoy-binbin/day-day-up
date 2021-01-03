# 146. LRU Cache LRU缓存机制

**<font color=red>难度: Medium</font>**

## 刷题内容

> 原题链接

* https://leetcode-cn.com/problems/lru-cache/

> 内容描述

```
运用你所掌握的数据结构，设计和实现一个  LRU (最近最少使用) 缓存机制 。

实现 LRUCache 类：
LRUCache(int capacity) 以正整数作为容量 capacity 初始化 LRU 缓存
int get(int key) 如果关键字 key 存在于缓存中，则返回关键字的值，否则返回 -1 。
void put(int key, int value) 如果关键字已经存在，则变更其数据值；如果关键字不存在，则插入该组「关键字-值」。当缓存容量达到上限时，它应该在写入新数据之前删除最久未使用的数据值，从而为新的数据值留出空间。

进阶：你是否可以在 O(1) 时间复杂度内完成这两种操作？

示例：
输入
["LRUCache", "put", "put", "get", "put", "get", "put", "get", "get", "get"]
[[2], [1, 1], [2, 2], [1], [3, 3], [2], [4, 4], [1], [3], [4]]
输出
[null, null, null, 1, null, -1, null, -1, 3, 4]

解释
LRUCache lRUCache = new LRUCache(2);
lRUCache.put(1, 1); // 缓存是 {1=1}
lRUCache.put(2, 2); // 缓存是 {1=1, 2=2}
lRUCache.get(1);    // 返回 1
lRUCache.put(3, 3); // 该操作会使得关键字 2 作废，缓存是 {1=1, 3=3}
lRUCache.get(2);    // 返回 -1 (未找到)
lRUCache.put(4, 4); // 该操作会使得关键字 1 作废，缓存是 {4=4, 3=3}
lRUCache.get(1);    // 返回 -1 (未找到)
lRUCache.get(3);    // 返回 3
lRUCache.get(4);    // 返回 4
 
提示：
1 <= capacity <= 3000
0 <= key <= 3000
0 <= value <= 104
最多调用 3 * 104 次 get 和 put
```

## 解题方案

> 方法零：使用OrderedDict，它实际上实现了哈希表跟双向链表，是内置数据结构

```python
class LRUCache(collections.OrderedDict):

    def __init__(self, capacity: int):
        super().__init__()
        self.capacity = capacity


    def get(self, key: int) -> int:
        if key not in self:
            return -1
        self.move_to_end(key)
        return self[key]

    def put(self, key: int, value: int) -> None:
        if key in self:
            self.move_to_end(key)
        self[key] = value
        if len(self) > self.capacity:
            self.popitem(last=False)
```



> 方法一：哈希表+双向链表

```python
class Node:
    def __init__(self, key: str, value: int):
        self.key = key  # 键
        self.value = value  # 值
        self.prev = None  # 指向前驱节点指针
        self.next = None  # 指向后继节点指针

    def __str__(self):
        return str((self.key, self.value))

class DoubleLinkedList:
    def __init__(self):
        self.size = 0  # 当前链表大小(长度)
        self.head = Node(key="head", value=0)  # 哑头节点
        self.tail = Node(key="tail", value=0)  # 哑尾节点
        self.head.next = self.tail  # 初始化头节点的后继为尾节点
        self.tail.prev = self.head  # 初始化尾节点的前驱为头节点
    
    def get_size(self):
        """ 获取链表长度, 时间复杂度O(1) """
        return self.size

    def add_node(self, node, direction=0):
        """ 往链表添加节点, 时间复杂度O(1) """
        if direction == 0:
            # 规定direction=0, 从表尾插入
            node.prev = self.tail.prev
            node.next = self.tail
            self.tail.prev.next = node
            self.tail.prev = node
            self.size += 1
            
        elif direction == 1:
            # 规定direction=1, 从表头插入(用不上)
            node.prev = self.head
            node.next = self.head.next
            self.head.next.prev = node
            self.head.next = node
            self.size += 1
    
    def remove_node(self, node):
        """ 往链表删除指定节点, 时间复杂度O(1) """
        node.prev.next = node.next
        node.next.prev = node.prev
        self.size -= 1
    
    def remove_first(self):
        """ 规定表头的数据是最久没使用的, 即最旧的, 淘汰并返回它, 时间复杂度O(1) """
        if self.head.next == self.tail:
            return None
        node = self.head.next
        self.remove_node(node)
        return node

    def __str__(self):
        """ 用于方便打印 """ 
        nodes = []
        if self.size > 0:
            node = self.head.next
            while node != self.head and node != self.tail:
                nodes.append(str(node))
                node = node.next
        return ", ".join(nodes)

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity  # 缓存容量
        self.map = dict()  # 哈希表 key -> node
        self.cache = DoubleLinkedList()  # 双向链表
    
    def make_recently(self, key):
        """ 将数据项放到最新的位置(表尾), 即最近使用过 """
        node = self.map.get(key)
        self.cache.remove_node(node)  # 删除节点
        self.cache.add_node(node)  # 重新插入表尾
        return node
    
    def add_recently(self, key, value):
        """ 添加最近使用过的数据项 """
        node = Node(key, value)
        self.cache.add_node(node)  # 表尾插入节点
        self.map[key] = node  # 哈希表映射关系
        return node
    
    def delete(self, key):
        """ 删除某个数据项 """
        node = self.map.get(key)
        self.cache.remove_node(node)  # 删除节点
        del self.map[key]  # 删除映射关系
        return node
    
    def delete_least_not_used(self):
        """ 删除最久未使用的数据项 """
        node = self.cache.remove_first()
        del self.map[node.key]
        return node

    def get_size(self):
        """ 获取实际缓存的大小, 即链表长度 """
        return self.cache.get_size()

    def put(self, key, value):
        """ 添加元素, 时间复杂度O(1) """
        if key not in self.map:
            # key不在缓存里, 新增加
            if self.get_size() == self.capacity:
                # 如果缓存满了, 需要先腾出位置
                self.delete_least_not_used()

            # 此时缓存没满, 直接加入
            self.add_recently(key, value)
        else:
            # key在缓存里, 更新它
            self.delete(key)
            self.add_recently(key, value)
    
    def get(self, key):
        """ 获取元素, 时间复杂度O(1) """
        if key not in self.map:
            return -1
        node = self.make_recently(key)
        return node.value
    
    def __str__(self):
        return str(self.cache)
```



> 方法二：哈希表+双向链表，简单版

```python
class Node:
    def __init__(self, key: int, value: int):
        self.key = key
        self.value = value
        self.next = None
        self.prev = None

class DoubleLinkedList:
    def __init__(self):
        self.size = 0
        self.head = Node(0, 0)
        self.tail = Node(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def remove_node(self, node):
        """ 删除一个节点 """
        node.prev.next = node.next
        node.next.prev = node.prev
        self.size -= 1
        node.prev = node.next = None

    def add_to_tail(self, node):
        """ 在尾部插入一个节点 """
        node.next = self.tail
        node.prev = self.tail.prev
        self.tail.prev.next = node
        self.tail.prev = node
        self.size += 1

    def move_to_tail(self, node):
        """ 将节点移动末端 """
        self.remove_node(node)
        self.add_to_tail(node)

class LRUCache:

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.map = dict()
        self.cache = DoubleLinkedList()

    def get(self, key: int) -> int:
        if key not in self.map:
            return -1
        node = self.map[key]
        self.cache.move_to_tail(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        if key not in self.map:
            if self.cache.size == self.capacity:
                # 满了, 需要删除一个元素, 可以直接传入head.next
                node = self.cache.head.next
                self.cache.remove_node(node)
                del self.map[node.key]
            node = Node(key, value)
            self.cache.add_to_tail(node)
            self.map[key] = node
        else:
            node = self.map[key]
            node.value = value
            self.cache.move_to_tail(node)
```
