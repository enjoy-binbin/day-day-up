# 938. Range Sum of BST 二叉搜索树的范围和

**<font color=red>难度: Easy</font>**

## 刷题内容

> 原题链接

* https://leetcode-cn.com/problems/range-sum-of-bst/

> 内容描述

```
给定二叉搜索树的根结点 root，返回 L 和 R（含）之间的所有结点的值的和。

二叉搜索树保证具有唯一的值。

示例 1：
输入：root = [10,5,15,3,7,null,18], L = 7, R = 15
输出：32

示例 2：
输入：root = [10,5,15,3,7,13,18,1,null,6], L = 6, R = 10
输出：23

提示：
树中的结点数量最多为 10000 个。
最终的答案保证小于 2^31。

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None
        
题目的意思有点奇怪的，其实是判断节点的值在范围内即可
```

## 解题方案

> 方法一：可以使用递归，遍历所有节点，后面优化可以剪枝

```python
class Solution:
    def __init__(self):
        self.result = 0

    def rangeSumBST(self, root: TreeNode, L: int, R: int) -> int:
        if not root:
            return 0

        self.helper(root, L, R)
        return self.result

    def helper(self, node, l, r):
        if not node:
            return

        if l <= node.val <= r:
            self.result += node.val

        self.helper(node.left, l, r)
        self.helper(node.right, l, r)
```



> 方法2：上面的迭代，同样遍历了所有节点

```python
class Solution:

    def rangeSumBST(self, root: TreeNode, L: int, R: int) -> int:
        if not root:
            return 0

        stack, result = [root], 0

        while stack:

            node = stack.pop()

            if L <= node.val <= R:
                result += node.val

            if node.left:
                stack.append(node.left)

            if node.right:
                stack.append(node.right)

        return result
```



> 方法三：迭代的剪枝版本

```python
class Solution:

    def rangeSumBST(self, root: TreeNode, L: int, R: int) -> int:
        if not root:
            return 0

        stack, result = [root], 0

        while stack:

            node = stack.pop()

            if node is None:
                continue

            if L <= node.val <= R:
                result += node.val

            if node.val > L:
                # 左子树的值都比node.val小
                stack.append(node.left)

            if node.val < R:
                # 右子树的值都比node.val大
                stack.append(node.right)

        return result
```



> 方法四：递归的剪枝版本

```python
class Solution:
    def __init__(self):
        self.result = 0

    def rangeSumBST(self, root: TreeNode, L: int, R: int) -> int:
        if not root:
            return 0

        self.helper(root, L, R)
        return self.result

    def helper(self, node, l, r):
        if not node:
            return

        if l <= node.val <= r:
            self.result += node.val

        if node.val > l:  
            self.helper(node.left, l, r)
        
        if node.val < r:
            self.helper(node.right, l, r)
```

