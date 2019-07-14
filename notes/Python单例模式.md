#### 单例模式

单例模式(Singleton Pattern)是一种常用的软件设计模式。在它的核心结构中只包含一个被称为单例类的特殊类。通过单例模式可以保证系统中一个类只有一个实例而且该实例易于外界访问，从而方便对实例个数的控制并节约系统资源。如果希望在系统中某个类的对象只能存在一个，单例模式是最好的解决方案。

1. 单例类只能有一个实例
2. 单例类必须自己创建自己的唯一实例
3. 单例类必须给所有其他对象提供这一个实例



#### Python单例模式的实现

##### 1. 使用`__new__()`

new方法是真正的实例化方法，在init之前被调用，用于生成实例对象，new必须要有返回值，返回一个实例化出来的实例

```python
class Singleton(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)

        return cls._instance


if __name__ == '__main__':
    obj = Singleton()
    obj2 = Singleton()
    print(obj2 is obj)  # True
```



##### 2. 使用装饰器修饰单例类

```python
def singleton(cls):
    instances = {}  # 存储一个个单例实例对象

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)

        return instances[cls]

    return get_instance


@singleton  # 注释掉输出是False
class Singleton(object):
    pass


if __name__ == '__main__':
    obj = Singleton()
    obj2 = Singleton()
    print(obj2 is obj)  # True
```



##### 3. 使用`__dict__`属性

Python中万物皆为对象，类的静态函数、类函数、普通函数、全局变量以及一些内置的属性都是放在`__dict__`属性里的，创建实例的时候把所有实例的`__dict__`指向同一个字典，这样他们就具有相同的属性和方法了

```python
class Singleton(object):
    _dic = {}

    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls, *args, **kwargs)
        obj.__dict__ = cls._dic
        return object


class Person(Singleton):
    pass


if __name__ == '__main__':
    obj = Person()
    obj2 = Person()
    print(obj2 is obj)  # True
```



##### 4. import引入实例对象

```python
# Singleton.py
class Singleton(object):
    pass


singleton_obj = Singleton()


# main.py
from Singleton import singleton_obj
```



##### 5. 使用classmethod装饰器

```python
class Singleton(object):
    _instance = None

    @classmethod
    def instance(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = cls(*args, **kwargs)

        return cls._instance


if __name__ == '__main__':
    obj = Singleton.instance()
    obj2 = Singleton.instance()
    print(obj is obj2)  # True
```



##### 6. 元类实现

`__call__()`实现后，类实例对象是可调用的，type()是Python中的元类。比较难讲清，放到另个元类笔记中讲，好像Django中的ORM有用到元类，改日再去拜读源码的实现，元类是实现类的类

```python
class Singleton(type):

    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class Person(metaclass=Singleton):
    pass


if __name__ == '__main__':
    obj = Person()
    obj2 = Person()
    print(obj is obj2)  # True
```





