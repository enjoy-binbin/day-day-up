# 144. Binary Tree Preorder Traversal 二叉树的前序遍历

**<font color=red>难度: Medium</font>**

## 刷题内容

> 原题链接

* https://leetcode-cn.com/problems/binary-tree-preorder-traversal/

> 内容描述

```
给定一个二叉树，返回它的 前序 遍历。

 示例:

输入: [1,null,2,3]  
   1
    \
     2
    /
   3 

输出: [1,2,3]
进阶: 递归算法很简单，你可以通过迭代算法完成吗？

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None
```

## 解题方案

> 方法一：递归前序遍历二叉树，没啥好说的了emm，时空复杂度O(n)

```python
class Solution:
    def __init__(self):
        self.res = []

    def preorderTraversal(self, root):
        if not root:
            return []
        self.helper(root)
        return self.res

    def helper(self, node):
        if not node:
            return

        self.res.append(node.val)
        self.helper(node.left)
        self.helper(node.right)
```



> 方法二：递归解法，时空复杂度O(n)

```python
class Solution:
    def preorderTraversal(self, root):
        if not root:
            return []

        stack, res = [root], []

        while stack:
            node = stack.pop()
            res.append(node.val)

            # 这里对于栈, 先进后出, 需要先压入右, 让左先出
            if node.right:
                stack.append(node.right)

            if node.left:
                stack.append(node.left)
        return res
```



> 方法三：莫里斯遍历

```python
class Solution(object):
    def preorderTraversal(self, root):
        """
        :type root: TreeNode
        :rtype: List[int]
        """
        node, output = root, []
        while node:  
            if not node.left: 
                output.append(node.val)
                node = node.right 
            else: 
                predecessor = node.left 

                while predecessor.right and predecessor.right is not node: 
                    predecessor = predecessor.right 

                if not predecessor.right:
                    output.append(node.val)
                    predecessor.right = node  
                    node = node.left  
                else:
                    predecessor.right = None
                    node = node.right         

        return output

作者：LeetCode
链接：https://leetcode-cn.com/problems/binary-tree-preorder-traversal/solution/er-cha-shu-de-qian-xu-bian-li-by-leetcode/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
```

