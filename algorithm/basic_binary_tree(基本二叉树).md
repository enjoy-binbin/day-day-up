#### Python实现简单的二叉树

树需要添加节点，广度优先遍历，深度优先遍历中的（先中后）

##### 代码实现

```python
class Node(object):
    """ Node节点 """

    def __init__(self, value):
        self.value = value  # 节点值
        self.left = None  # 左孩子
        self.right = None  # 右孩子


class BinaryTree(object):
    def __init__(self):
        self.root = None

    def add(self, value):
        node = Node(value)

        # 如果没有根节点
        if self.root is None:
            self.root = node
            return None

        queue = [self.root]
        while queue:
            cur_node = queue.pop(0)

            # 如果左子树为空，就将节点加入左子树
            if not cur_node.left:
                cur_node.left = node
                return None
            else:
                queue.append(cur_node.left)

            # 如果右子树为空，就将节点加入右子树
            if not cur_node.right:
                cur_node.right = node
                return None
            else:
                queue.append(cur_node.right)

    def bread_travel(self):
        """ 广度遍历 """
        if not self.root:
            return None

        queue = [self.root]
        while queue:
            cur_node = queue.pop(0)
            print(cur_node.value, end=' ')

            if cur_node.left:
                queue.append(cur_node.left)
            if cur_node.right:
                queue.append(cur_node.right)

    def pre_travel(self, node):
        """ 前序遍历，中左右 """
        if not node:
            return None
        print(node.value, end=' ')
        self.pre_travel(node.left)
        self.pre_travel(node.right)

    def mid_travel(self, node):
        """ 中序遍历，左中右 """
        if not node:
            return None
        self.mid_travel(node.left)
        print(node.value, end=' ')
        self.mid_travel(node.right)

    def post_travel(self, node):
        """ 后序遍历，左右中 """
        if not node:
            return None
        self.post_travel(node.left)
        self.post_travel(node.right)
        print(node.value, end=' ')


if __name__ == '__main__':
    binary_tree = BinaryTree()
    binary_tree.add(0)
    binary_tree.add(1)
    binary_tree.add(2)
    binary_tree.add(3)
    binary_tree.add(4)

    binary_tree.bread_travel()  # 0 1 2 3 4
    print('')

    binary_tree.pre_travel(binary_tree.root)  # 0 1 3 4 2
    print('')

    binary_tree.mid_travel(binary_tree.root)  # 3 1 4 0 2
    print('')

    binary_tree.post_travel(binary_tree.root)  # 3 4 1 2 0
    print('')
    
    # 树的形状
    #       		 0
    #   	  1			  2
    #	  3	    4
    # 广度遍历：0 1 2 3 4
    # 先序遍历：0 1 3 4 2
    # 中序遍历：3 1 4 0 2
    # 后序遍历：3 4 1 2 0
```

