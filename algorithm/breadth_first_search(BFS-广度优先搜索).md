#### 广度优先搜索

##### 一、前言

BFS是一种利用**队列**实现的搜索算法。简单来说，其搜索过程和 “湖面丢进一块石头激起层层涟漪” 类似。

队列是`FIFO`的，First In First Out 先进先出。

BFS指出是否有从A到B的路径，如果有，找出最短路径（图），图有有向图、无向图、加权图等

BFS 常用于找单一的最短路线，它的特点是 "搜到就是最优解"

就用leetcode里的102题解释



##### 二、例题

```
# https://leetcode-cn.com/problems/binary-tree-level-order-traversal/
给定一个二叉树，返回其按层次遍历的节点值。 （即逐层地，从左到右访问所有节点）。

例如:
给定二叉树: [3,9,20,null,null,15,7],

    3
   / \
  9  20
    /  \
   15   7

返回其层次遍历结果：

[
  [3],
  [9,20],
  [15,7]
]
```



##### 三、代码实现

使用BFS（Breath First Search）广度优先搜索，一层一层的遍历，如例子就是 3-9-20-15-7 时间复杂度O(n)，对于每个节点只访问一次

```python
import collections

class Solution(object):
    def levelOrder(self, root):
        """
        :type root: TreeNode
        :rtype: List[List[int]]
        """
        # BFS 广度优先搜索 Breath First Search
        if not root:
            return []

        res = []  # 返回的结果, [[],[]] 存储着一层一层的
        queue = collections.deque()  # 一个双端队列
        queue.append(root)  # 先把头节点append进去 第一层

        while queue:
            level = []  # 当前层
            level_size = len(queue)  # 当前层的节点数目

            for i in range(level_size):
                node = queue.popleft()  # 左边弹出
                level.append(node.val)

                # 如果左右节点存在, 就加进queue中, 进行下一层的遍历
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

            res.append(level)  # 将当前层append进结果列表中

        return res
```



##### 四、说明点

关于BFS和DFS，都是很重要的算法，多写题吧