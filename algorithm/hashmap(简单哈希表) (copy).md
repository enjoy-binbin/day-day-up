#### Python实现简单的哈希表

MyHash内部使用items列表来存储数据，items是一个列表，并且每个子元素也是一个列表，元素列表中存储了具体的(key, value)元组元素。

不同的数字key根据hash函数取余计算得出index，表示存储在哪个子列表中。插入时直接插入，更新时先遍历找处旧元素删除再添加，(id内存空间会变)，查找的时候也是遍历找到对应的key和value

##### 代码实现

```python
class MyHash(object):
    def __init__(self, length=10):
        """ 根据长度构建好二维空列表 """
        self.length = length
        self.items = [[] for _ in range(self.length)]

    def hash(self, key):
        """ 计算该key在items哪个list中，现在只支持int作为key """
        return key % self.length

    def insert(self, key, value):
        index = self.hash(key)
        if self.items[index]:
            for item in self.items[index]:
                if key == item[0]:
                    # 添加元素时，如果key存在，则先删除后添加（更新value)
                    # 对于python中字典也是，如果元素改变了，id(dict['key'])也是会变的
                    self.items[index].remove(item)
                    break

        self.items[index].append((key, value))  # 存储的是元组 [(k, v), (k, v)]
        return True

    def get(self, key):
        """ 获取指定key的value """
        index = self.hash(key)
        if self.items[index]:
            for item in self.items[index]:
                if key == item[0]:
                    return item[1]

        # 找不到key，则抛出KeyError异常
        raise KeyError

    def __setitem__(self, key, value):
        """ 支持 my_hash[key] = value 添加 """
        return self.insert(key, value)

    def __getitem__(self, key):
        """ my_hash[key] 获取value """
        return self.get(key)


if __name__ == '__main__':
    my_hash = MyHash()

    my_hash.insert(1, 'key为1')
    print(my_hash.get(1))

    my_hash.insert(66, 'key为66')
    print(my_hash.get(66))

    my_hash[88] = 'key为88'
    print(my_hash[88])

    my_hash[36] = 'key为36'

    # [[], [(1, 'key为1')], [], [], [], [], [(66, 'key为66'), (36, 'key为36')], [], [(88, 'key为88')], []]
    print(my_hash.items)
```

输出结果：

```
key为1
key为66
key为88
[[], [(1, 'key为1')], [], [], [], [], [(66, 'key为66'), (36, 'key为36')], [], [(88, 'key为88')], []]
```

