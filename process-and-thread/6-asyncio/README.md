#### asyncio

------

`asyncio`是Python 3.4版本引入的标准库，直接内置了对异步IO的支持。

`asyncio`的编程模型就是一个消息循环。我们从`asyncio`模块中直接获取一个`EventLoop`的引用，然后把需要执行的协程扔到`EventLoop`中执行，就实现了异步IO。

用`asyncio`实现`Hello world`代码如下：

```python
import asyncio
import time
import threading


@asyncio.coroutine  # 会把一个生成器标记为coroutine类型
def hello():
    print("Hello world! (%s)" % threading.currentThread())

    # 异步调用asyncio.sleep(2):
    yield from asyncio.sleep(2)

    print("Hello again! (%s)" % threading.currentThread())


if __name__ == '__main__':
    start = time.time()
    # 获取EventLoop:
    loop = asyncio.get_event_loop()
    # 执行coroutine
    loop.run_until_complete(hello())
    loop.close()
    print('times: %0.4f seconds' % (time.time() - start))
```

运行结果：

```powershell
Hello world! (<_MainThread(MainThread, started 1276)>)
Hello again! (<_MainThread(MainThread, started 1276)>)
times: 2.0020 seconds
```

`@asyncio.coroutine`把一个generator标记为coroutine类型，然后，我们就把这个`coroutine`扔到`EventLoop`中执行。

`hello()`会首先打印出`Hello world!`，然后，`yield from`语法可以让我们方便地调用另一个`generator`。由于`asyncio.sleep()`也是一个`coroutine`，所以线程不会等待`asyncio.sleep()`，而是直接中断并执行下一个消息循环。当`asyncio.sleep()`返回时，线程就可以从`yield from`拿到返回值（此处是`None`），然后接着执行下一行语句。

把`asyncio.sleep(1)`看成是一个耗时1秒的IO操作，在此期间，主线程并未等待，而是去执行`EventLoop`中其他可以执行的`coroutine`了，因此可以实现并发执行。

我们用Task封装两个`coroutine`试试：

```python
import asyncio
import time
import threading


@asyncio.coroutine  # 会把一个生成器标记为coroutine类型
def hello():
    print("Hello world! (%s)" % threading.currentThread())

    # 异步调用asyncio.sleep(2):
    yield from asyncio.sleep(2)

    print("Hello again! (%s)" % threading.currentThread())


if __name__ == '__main__':
    start = time.time()
    # 获取EventLoop:
    loop = asyncio.get_event_loop()
    # 执行coroutine
    tasks = [hello(), hello()]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
    print('times: %0.4f seconds' % (time.time() - start))
```

观察执行过程：

```powershell
Hello world! (<_MainThread(MainThread, started 8972)>)
Hello world! (<_MainThread(MainThread, started 8972)>)
# 这里暂停两秒，不会等待asyncio.sleep，而会去执行另外个消息循环
Hello again! (<_MainThread(MainThread, started 8972)>)
Hello again! (<_MainThread(MainThread, started 8972)>)
times: 2.0020 seconds
```

由打印的当前线程名称可以看出，两个`coroutine`是由同一个线程并发执行的。

如果把`asyncio.sleep()`换成真正的IO操作，则多个`coroutine`就可以由一个线程并发执行。

我们用`asyncio`的异步网络连接来获取sina、sohu和163的网站首页：

```python
import asyncio


@asyncio.coroutine
def wget(host):
    print('wget %s...' % host)
    connect = asyncio.open_connection(host, 80)
    reader, writer = yield from connect
    header = 'GET / HTTP/1.0\r\nHost: %s\r\n\r\n' % host
    writer.write(header.encode('utf-8'))
    yield from writer.drain()
    while True:
        line = yield from reader.readline()
        if line == b'\r\n':
            break
        print('%s header > %s' % (host, line.decode('utf-8').rstrip()))
    # Ignore the body, close the socket
    writer.close()


if __name__ == '__main__':
    # 获取EventLoop
    loop = asyncio.get_event_loop()

    # 执行coroutine
    tasks = [wget(host) for host in ['www.sina.com.cn', 'www.sohu.com', 'www.163.com']]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
```

执行结果如下：

```
wget www.sohu.com...
wget www.sina.com.cn...
wget www.163.com...
(等待一段时间)
(打印出sohu的header)
www.sohu.com header > HTTP/1.1 200 OK
www.sohu.com header > Content-Type: text/html
...
(打印出sina的header)
www.sina.com.cn header > HTTP/1.1 200 OK
www.sina.com.cn header > Date: Wed, 20 May 2015 04:56:33 GMT
...
(打印出163的header)
www.163.com header > HTTP/1.0 302 Moved Temporarily
www.163.com header > Server: Cdn Cache Server V2.0
...
```

可见3个连接由一个线程通过`coroutine`并发完成。

### 小结

`asyncio`提供了完善的异步IO支持；

异步操作需要在`coroutine`中通过`yield from`完成；

多个`coroutine`可以封装成一组Task然后并发执行。



#### async/await

用`asyncio`提供的`@asyncio.coroutine`可以把一个generator标记为coroutine类型，然后在coroutine内部用`yield from`调用另一个coroutine实现异步操作。

为了简化并更好地标识异步IO，从Python 3.5开始引入了新的语法`async`和`await`，可以让coroutine的代码更简洁易读。

请注意，`async`和`await`是针对coroutine的新语法，要使用新的语法，只需要做两步简单的替换：

1. 把`@asyncio.coroutine`替换为`async`；
2. 把`yield from`替换为`await`。

让我们对比一下上一节的代码：

```
@asyncio.coroutine
def hello():
    print("Hello world!")
    r = yield from asyncio.sleep(1)
    print("Hello again!")
```

用新语法重新编写如下：

```
async def hello():
    print("Hello world!")
    r = await asyncio.sleep(1)
    print("Hello again!")
```

剩下的代码保持不变。

### 小结

Python从3.5版本开始为`asyncio`提供了`async`和`await`的新语法；

注意新语法只能用在Python 3.5以及后续版本，如果使用3.4版本，则仍需使用上一节的方案。