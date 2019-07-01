#### 广度优先搜索

##### 一、前言

DFS是一种利用**递归**实现的搜索算法。简单来说，其搜索过程和 “不撞南墙不回头” 类似。

DFS用于找出一个问题的所有解，会记录所有问题解，一般来说，需要配合高效的剪枝，剪枝就是剪掉一些不必要的，不会产生答案的枝条剪掉。

使用leetcode里的102题解释



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

使用DFS（Depth First Search）深度优先搜索，一条路走到底，时间复杂度O(n)，节点只访问一次

```python
class Solution(object):

    def levelOrder(self, root):
        """
        :type root: TreeNode
        :rtype: List[List[int]]
        """
        if not root:
            return []

        # 递归解法, 深度优先搜索, DFS(Death First Search)
        self.res = []
        self.helper(root, 0)
        return self.res

    def helper(self, node, level):
        if not node:
            return None
        if len(self.res) == level:  # root进来是0, res = [[第一层], [第二层]]
            self.res.append([])  # 创建当前层列表

        self.res[level].append(node.val)
        self.helper(node.left, level + 1)
        self.helper(node.right, level + 1)
```



##### 四、说明点

关于BFS和DFS，都是很重要的算法，多写题吧