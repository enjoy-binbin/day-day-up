这部分内容参考自廖雪峰教程

#### 1. linux下的os.fork()函数

要让Python程序实现多进程（multiprocessing），我们先了解操作系统的相关知识。

Unix/Linux操作系统提供了一个`fork()`系统调用，它非常特殊。普通的函数调用，调用一次，就返回一次。

但是`fork()`调用一次，会返回两次，因为操作系统自动把当前进程（称为父进程）复制了一份（称为子进程），然后，分别在父进程和子进程内返回。

子进程永远返回`0`，而父进程会返回子进程的ID。这样做的理由是，一个父进程可以fork出很多子进程，所以，父进程要记下每个子进程的ID，而子进程只需要调用`getppid()`就可以拿到父进程的ID。

Python的`os`模块封装了常见的系统调用，其中就包括`fork`，可以在Python程序中轻松创建子进程：以下代码需要在linux下执行，因为win下没有fork函数

```python
import os

print('Process (%s) start ...' % os.getpid())

pid = os.fork()  # 子进程会返回0, 父进程会返回子进程的pid

if pid == 0:
    print('i am a child proccess (%s) and my parent is (%s)' % (os.getpid(), os.getppid()))
else:
    print('i (%s) just created a child process (%s)' % (os.getpid(), pid))
```

运行结果如下：

```shell
[root@localhost ~]# python multiprocessing.py 
Process (6588) start ...
i (6588) just created a child process (6589)
i am child (6589), my parent is (6588)
```

有了`fork`调用，一个进程在接到新任务时就可以复制出一个子进程来处理新任务，常见的Apache服务器就是由父进程监听端口，每当有新的http请求时，就fork出子进程来处理新的http请求。



#### 2. Python中的multiprocessing模块

在Python中有跨平台的multiprocessing模块进行多进程的实现，创建子进程的时候，只需要传入一个执行函数和函数对应的参数，创建`Process`实例，用`start`方法启动，而`join`方法是主进程会等待子进程结束才会继续执行，常用于进程间的同步。

```python
import os
from multiprocessing import Process


# 子进程执行的函数
def run_proc(name):
    print('Run child process %s (%s)...' % (name, os.getpid()))


if __name__ == '__main__':
    print('Parent process is (%s).' % os.getpid())

    # 创建进程, 传入需要执行的函数, 和函数对应的参数
    p = Process(target=run_proc, args=('test',))
    print('Process start.')
    p.start()  # 启动进程
    p.join()  # 主进程会等待子进程的结束
    print('Process end.')
```

输出结果，需要到命令行下执行

```powershell
D:\a\day-day-up\process-and-thread (master -> origin)
λ python 1-2-multiprocessing.py
Parent process is (3816).
Process start.
Run child process test (10916)...
Process end.
```

注释掉join那行后的输出结果

```powershell
D:\a\day-day-up\process-and-thread (master -> origin)
λ python 1-2-multiprocessing.py
Parent process is (8304).
Process start.
Process end.
Run child process test (10024)...
```



#### 3. Pool进程池

可以使用进程池的方式批量创建子进程

```python
import os, time, random
from multiprocessing import Pool


def long_time_task(name):
    print('Run task %s (%s)...' % (name, os.getpid()))
    start = time.time()
    # time.sleep(1)  # 可以取消注释查看运行效果
    time.sleep(random.random() * 3)  # random() 随机返回0-1之间数
    end = time.time()
    print('Task %s runs %0.2f seconds.' % (name, (end - start)))


if __name__ == '__main__':
    start = time.time()
    print('Parent process %s.' % os.getpid())

    p = Pool()
    for i in range(5):  # 创建5个进程，因为当前电脑是四核CPU，所以会有个进程会等待，看后面的结果
        p.apply_async(long_time_task, args=(i,))  # 异步非阻塞
        # p.apply(long_time_task, args=(i,))  # 阻塞，得等子进程执行完才执行下一个进程

    print('Waiting for all subprocesses done...')
    p.close()  # 对pool调用close后之后就不能再添加新的进程
    p.join()  # 对pool调用join前必须先close, 会等待所有子进程完成
    print('All subprocesses done.')

    print('Total time %0.2f seconds' % (time.time() - start))
```

运行结果，可以看到 `task4`是在`tak3`完成后才执行，因为本机是四核CPU，Pool默认大小为4，最多同时执行四个进程，这是因为Pool默认大小是系统CPU核数，如果改成`p = Pool(5)`就可以同时跑5个进程了，可以自己动手实验下。而对于`apply`和`apply_async`，前者是阻塞(基本不用)，后者是异步非阻塞，看后面的结果实验下即可

```powershell
D:\a\day-day-up\process-and-thread (master -> origin)
λ python 1-3-pool.py
Parent process 9532.
Waiting for all subprocesses done...
Run task 0 (9620)...
Run task 1 (9232)...
Run task 2 (5884)...
Run task 3 (9740)...
Task 3 runs 0.31 seconds.
Run task 4 (9740)...
Task 4 runs 0.23 seconds.
Task 1 runs 0.72 seconds.
Task 2 runs 0.79 seconds.
Task 0 runs 1.79 seconds.
All subprocesses done.
Total time 1.99 seconds

# Pool(5)
D:\a\day-day-up\process-and-thread (master -> origin)
λ python 1-3-pool.py
Parent process 8300.
Waiting for all subprocesses done...
Run task 0 (8024)...
Run task 1 (1072)...
Run task 2 (6984)...
Run task 3 (4140)...
Run task 4 (2852)...
Task 2 runs 0.29 seconds.
Task 0 runs 1.20 seconds.
Task 3 runs 1.59 seconds.
Task 1 runs 2.50 seconds.
Task 4 runs 2.93 seconds.
All subprocesses done.
Total time 3.69 seconds

# apply阻塞
D:\a\day-day-up\process-and-thread (master -> origin)
λ python 1-3-pool.py
Parent process 9068.
Run task 0 (7844)...
Task 0 runs 1.03 seconds.
Run task 1 (9184)...
Task 1 runs 0.62 seconds.
Run task 2 (8276)...
Task 2 runs 0.45 seconds.
Run task 3 (9716)...
Task 3 runs 0.83 seconds.
Run task 4 (7844)...
Task 4 runs 2.76 seconds.
Waiting for all subprocesses done...
All subprocesses done.
Total time 5.86 seconds
```



#### 4. 进程通信

`Process`进程之间肯定是需要通信的，操作系统提供了很多机制来实现进程间的通信。`multiprocessing`模块包装了底层的机制，提供了`Queue`、`Pipes`等多种方式来交换数据。

下面以`Queue`为例，在父进程中创建两个子进程，一个往队列里写数据，另一个从里面读取数据。

```python
import time
import random
from multiprocessing import Process, Queue


# 写数据进程执行的函数
def write(q):
    for value in ['value_1', 'value_2', 'value_3']:
        print('Put %s to queue...' % value)
        q.put(value)
        time.sleep(random.random() * 2)


# 读数据进程执行的函数
def read(q):
    while True:
        value = q.get(True)
        print('Get %s from queue.' % value)


if __name__ == '__main__':
    start = time.time()

    # 父进程创建Queue，并传给各个子进程：
    queue = Queue()
    p_write = Process(target=write, args=(queue,))
    p_read = Process(target=read, args=(queue,))
    # 启动子进程pw, 写入数据
    p_write.start()
    # 启动子进程pr，读取数据
    p_read.start()
    # 等待pw结束
    p_write.join()
    # pr进程里是死循环，无法等待其结束，只能强行终止
    p_read.terminate()

    print('Done %0.2f seconds' % (time.time() - start))
```

运行结果

```powershell
D:\a\day-day-up\process-and-thread (master -> origin)
λ python 1-4-Queue.py
Put value_1 to queue...
Get value_1 from queue.
Put value_2 to queue...
Get value_2 from queue.
Put value_3 to queue...
Get value_3 from queue.
Done 4.04 seconds
```

