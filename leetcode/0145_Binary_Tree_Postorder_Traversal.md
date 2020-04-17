# 145. Binary Tree Preorder Traversal 二叉树的前序遍历

**<font color=red>难度: Difficult</font>**

## 刷题内容

> 原题链接

* https://leetcode-cn.com/problems/binary-tree-postorder-traversal/

> 内容描述

```
给定一个二叉树，返回它的 后序 遍历。

示例:

输入: [1,null,2,3]  
   1
    \
     2
    /
   3 

输出: [3,2,1]
进阶: 递归算法很简单，你可以通过迭代算法完成吗？

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None
后序遍历：左右中
```

## 解题方案

> 方法零：后续遍历迭代写法

```python
class Solution:
    def postorderTraversal(self, root):
        # 后序遍历, 左右中
        if not root:
            return []
        result, stack = [], []
        current, last = root, None

        while current or stack:
            if current:
                # 将所有的左入栈
                stack.append(current)
                current = current.left
            else:
                # 取出栈顶元素
                node = stack[-1]
                # 判断是否需要变到右子树, 同时判断上次遍历的元素不能为自己的右(从右边来)
                if node.right and node.right != last:
                    current = node.right
                else:
                    result.append(node.val)
                    last = node
                    stack.pop()

        return result
```



> 方法零：推两次节点

```python
class Solution:
    def postorderTraversal(self, root):
        if not root:
            return []
        result, stack = [], []

        stack.append(root)
        stack.append(root)

        while stack:
            current = stack.pop()
            if current and stack[-1] is current:
                if current.right:
                    stack += [current.right] * 2
                if current.left:
                    stack += [current.left] * 2
            else:
                result.append(current.val)

        return result
```



> 方法一：跟其他遍历题目是一个意思，只是需要注意列表pop的时候的顺序

```python
class Solution:
    def postorderTraversal(self, root):
        if not root:
            return []

        stack, result = [root], []

        while stack:
            node = stack.pop()
            result.append(node.val)

            if node.left:
                stack.append(node.left)
            if node.right:
                stack.append(node.right)

        return result[::-1]
```



> 方法二：递归前序遍历解法，时空复杂度O(n)

```python
class Solution:
    def __init__(self):
        self.result = []

    def postorderTraversal(self, root):
        if not root:
            return []
        self.helper(root)
        return self.result[::-1]

    def helper(self, node):
        if not node:
            return

        self.result.append(node.val)
        if node.right:
            self.helper(node.right)
        if node.left:
            self.helper(node.left)
```



> 方法三：递归后序遍历

```python
class Solution:
    def __init__(self):
        self.result = []

    def postorderTraversal(self, root):
        if not root:
            return []
        self.helper(root)
        return self.result

    def helper(self, node):
        if not node:
            return
        if node.left:
            self.helper(node.left)
        if node.right:
            self.helper(node.right)
        self.result.append(node.val)
```

