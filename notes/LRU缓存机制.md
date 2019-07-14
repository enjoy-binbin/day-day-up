#### LRU

LRU（Least Recently Used），即最近最少使用

简单的说在有限的空间中，淘汰掉最近最少使用的元素。



#### 面试题：**出题人**：文景／阿里云 CDN 资深技术专家

LRU 缓存机制 设计和实现一个 LRU（最近最少使用）缓存数据结构，使它应该支持一下操作：get 和 put。 get(key) - 如果 key 存在于缓存中，则获取 key 的 value（总是正数），否则返回 -1。 put(key,value) - 如果 key 不存在，请设置或插入 value。当缓存达到其容量时，它应该在插入新项目之前使最近最少使用的项目作废。

#### 参考答案(py3)

```python
class LRUCache(object):
    def __init__(self, capacity):
        """
        :type capacity: int
        """
        self.cache = {}  # LRU缓存 {key: value}
        self.keys = []  # 队列存储缓存中所有的key，使用队列 保存key的使用关系，尾进头出
        self.capacity = capacity  # 缓存的容量

    def get(self, key):
        if not key in self.keys:
            return -1
        self.visit_key(key)
        return self.cache[key]

    def put(self, key, value):
        if not key in self.cache:
            # 不存在就设置
            if len(self.keys) == self.capacity:
                self.elim_key()
            self.visit_key(key)
            self.cache[key] = value
        else:
            # 存在就更新
            self.visit_key(key)
            self.cache[key] = value

    def visit_key(self, key):
        """ 使用了某个key，将其移除再添加，放到缓存末尾 """
        if key in self.keys:
            self.keys.remove(key)
        self.keys.append(key)

    def elim_key(self):
        """ 删除缓存中一个头元素(最近最少使用) """
        key = self.keys[0]
        self.keys = self.keys[1:]  # keys.remove(key)
        del self.cache[key]


def main():
    s = [
        ["put", "put", "get", "put", "get", "put", "get", "get", "get"],  # 操作
        [[1, 1], [2, 2], [1], [3, 3], [2], [4, 4], [1], [3], [4]]  # 值
    ]
    obj = LRUCache(2)
    result = []

    # 01 前两个put: obj = {1:1, 2:2}
    # 2 第一个get: res = [1], obj = {2:2, 1:1}
    # 3 第三个put: obj = {2:2, 3:3}
    # 4 第二个get: res = [1, -1], obj = {2:2, 1:1}
    # 5 第四个put: res = {3:3, 4:4}
    # 6 第三个get: res = [1, -1, -1]
    # 7 第四个get: res = [1, -1, -1, 3], obj = {4:4, 3:3}
    # 8 第五个gedaant: res = [1, -1, -1, 3, 4], obj = {3:3, 4:4}
    for i, c in enumerate(s[0]):
        if c == "get":
            result.append(obj.get(s[1][i][0]))
        elif c == 'put':
            # put(key, value)
            obj.put(s[1][i][0], s[1][i][1])
    print(result)  # [1, -1, -1, 3, 4]
    print(obj.cache)  # {3: 3, 4: 4}


if __name__ == "__main__":
    main()

```



### 一个自己实现的LRU缓存类

```python
import time
from collections import OrderedDict  # 一个有序的Dict
from functools import wraps


class LRUCacheDict(object):
    # py3: from functools import lru_cache
    def __init__(self, max_size=1024, expiration=60):
        self.max_size = max_size  # 最大容量, 1024个key
        self.expiration = expiration  # 单个key有效期60秒
        self._cache = {}  # LRU缓存 (Least Recently Used 近期最少使用)
        self._access_time = OrderedDict()  # 记录访问时间
        self._expire_time = OrderedDict()  # 记过过期时间

    def __setitem__(self, key, value):
        """ 设置缓存, 调用obj[key] = value执行 """
        now = int(time.time())
        self.__delitem__(key)  # 删除当前key

        self._cache[key] = value
        self._access_time[key] = now
        self._expire_time[key] = now + self.expiration
        self.cleanup()

    def __getitem__(self, key):
        """ 获取缓存中key对应的value, 调用obj['key']执行 """
        now = int(time.time())
        del self._access_time[key]

        self._access_time[key] = now
        self.cleanup()

        return self._cache[key]

    def __delitem__(self, key):
        """ 调用 del obj['key']时候执行 """
        if key in self._cache:
            del self._cache[key]
            del self._access_time[key]
            del self._expire_time[key]

    def __contains__(self, key):
        """ 当前缓存中是否有这个key, 当调用key in obj会执行 """
        self.cleanup()
        return key in self._cache

    def cleanup(self):
        """ 清理过期或者超过大小的缓存 """
        if self.expiration is None:
            return None  # 没设置过期时间就不清理

        now = int(time.time())
        pending_del_keys = []  # 存储待删除的key

        # 记录过期缓存key
        for key, value in self._expire_time.items():
            if value < now:
                pending_del_keys.append(key)

        # 删除过期缓存key, 因为不能在上面迭代过程中删除
        for del_key in pending_del_keys:
            self.__delitem__(del_key)

        # 超过容量, 删除最旧的缓存
        while len(self._cache) > self.max_size:
            for key in self._access_time:
                self.__delitem__(key)
                break

    def size(self):
        """ 返回缓存长度 """
        return len(self._cache)

    def clear(self):
        """ 清理所有缓存 """
        self._cache.clear()
        self._access_time.clear()
        self._expire_time.clear()


def cache_it(max_size=1024, expiration=60):
    cache = LRUCacheDict(max_size, expiration)

    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            key = repr(*args, **kwargs)
            try:
                result = cache[key]
            except KeyError:
                result = func(*args, **kwargs)
                cache[key] = result
            return result

        return inner

    return wrapper


@cache_it(max_size=2, expiration=2)
def test(num):
    time.sleep(1)  # 睡一秒, 只有第一次没缓存的时候慢
    res = 'this is number %s' % num
    return res


if __name__ == '__main__':
    cache_dict = LRUCacheDict(max_size=3, expiration=1)
    cache_dict['name'] = 'binbin'
    cache_dict['age'] = '22'
    cache_dict['gender'] = 'male'
    cache_dict['other'] = 'null'

    print('name' in cache_dict)  # False, 超过最大容量, 最旧的记录被删除了
    print('other' in cache_dict)  # True
    time.sleep(1.5)
    print('other' in cache_dict)  # Fasle, 过期记录被删除了

    print(test(2))
    print(test(3))
    print(test(2))  # 这里就直接用到了缓存, 没有sleep(1)
```

