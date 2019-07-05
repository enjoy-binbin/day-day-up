#### 1. threading多线程

多任务可以由多进程完成，也可以由一个进程内的多线程完成。

我们前面提到了进程是由若干线程组成的，一个进程至少有一个线程。

由于线程是操作系统直接支持的执行单元，因此，高级语言通常都内置多线程的支持，Python也不例外，并且，Python的线程是真正的Posix Thread，而不是模拟出来的线程。

Python的标准库提供了两个模块：`thread`和`threading`，`thread`是低级模块，`threading`是高级模块，对`thread`进行了封装。绝大多数情况下，我们只需要使用`threading`这个高级模块。

启动一个线程就是把一个函数传入并创建`Thread`实例，然后调用`start()`开始执行：

```python
import time
import threading


# 新线程执行的代码:
def loop():
    print('thread %s is running...' % threading.current_thread().name)
    n = 0
    while n < 5:
        n = n + 1
        print('thread %s >>> %s' % (threading.current_thread().name, n))
        time.sleep(1)
    print('thread %s ended.' % threading.current_thread().name)

if __name__ == '__main__':
	# 主线程
	print('thread %s is running...' % threading.current_thread().name)

	# 创建了一个新线程 名为 LoopThread
	t = threading.Thread(target=loop, name='LoopThread')
	t.start()
	t.join()
	print('thread %s ended.' % threading.current_thread().name)
```

运行结果：

```powershell
D:\a\day-day-up\process-and-thread (master -> origin)
λ python 2-1-thread.py
thread MainThread is running...
thread LoopThread is running...
thread LoopThread >>> 1
thread LoopThread >>> 2
thread LoopThread >>> 3
thread LoopThread >>> 4
thread LoopThread >>> 5
thread LoopThread ended.
thread MainThread ended.
```

由于任何进程默认就会启动一个线程，我们把该线程称为主线程，主线程又可以启动新的线程，Python的`threading`模块有个`current_thread()`函数，它永远返回当前线程的实例。主线程实例的名字叫`MainThread`，子线程的名字在创建时指定，我们用`LoopThread`命名子线程。名字仅仅在打印时用来显示，完全没有其他意义，如果不起名字Python就自动给线程命名为`Thread-1`，`Thread-2`……



#### 2. Lock锁

多线程和多进程最大的不同在于，多进程中，同一个变量，各自有一份拷贝存在于每个进程中，互不影响，而多线程中，变量是共享的，所以，任何一个变量都可以被其他线程修改，因此，线程之间共享数据最大的危险在于多个线程同时改一个变量，把内容给改乱了。

来看看多个线程同时操作一个变量怎么把内容给改乱了，下面代码需要多执行几次

```python
import time
import threading

# 我有0块钱
money = 0

def change_it(n):
    # 先存后取，最后结果应该是为0
    global money  # 声明全局变量，局部变量其他线程是看不到的
    money = money + n
    money = money - n

# 线程执行的函数
def run_thread(n):
    for i in range(100000):
        change_it(n)

if __name__ == '__main__':
	t1 = threading.Thread(target=run_thread, args=(5,))
	t2 = threading.Thread(target=run_thread, args=(10,))
	t1.start()
	t2.start()
	t1.join()
	t2.join()
	print(money)
```

运行结果，根据代码函数中先加后减，理论上值是不变的，可是由于线程是系统调度的，但两个线程交替执行时候，就会有可能出现问题。原因是高级语言在执行这样的赋值语句的时候`a = a + n`时也会分成两步`temp = a+n ` 和 `a = temp`，会先计算等号右边的值，再赋值

```powershell
D:\a\day-day-up\process-and-thread (master -> origin)
λ python 2-2-lock.py
0

D:\a\day-day-up\process-and-thread (master -> origin)
λ python 2-2-lock.py
10
```

所以在这种情况下，需要引入锁的概念，要给`change_it()`上一把锁，当某个线程开始执行`change_it()`时，我们说，该线程因为获得了锁，因此其他线程不能同时执行`change_it()`，只能等待，直到锁被释放后，获得该锁以后才能改。由于锁只有一个，无论多少线程，同一时刻最多只有一个线程持有该锁，所以，不会造成修改的冲突。创建一个锁就是通过`threading.Lock()`来实现

```python
import time
import threading

# 我有0块钱
money = 0
lock = threading.Lock()

def change_it(n):
    # 先存后取，最后结果应该是为0
    global money  # 声明全局变量
    money = money + n
    money = money - n

# 线程执行的函数
def run_thread(n):
    for i in range(100000):
        lock.acquire()  # 加锁
        try:
            change_it(n)
        finally:
            lock.release()  # 最后记得要释放锁

if __name__ == '__main__':
    t1 = threading.Thread(target=run_thread, args=(5,))
    t2 = threading.Thread(target=run_thread, args=(10,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print(money)
```

当多个线程同时执行`lock.acquire()`时，只有一个线程能成功地获取锁，然后继续执行代码，其他线程就继续等待直到获得锁为止。

获得锁的线程用完后一定要释放锁，否则那些苦苦等待锁的线程将永远等待下去，成为死线程。所以我们用`try...finally`来确保锁一定会被释放。

锁的好处就是确保了某段关键代码只能由一个线程从头到尾完整地执行，坏处当然也很多，首先是阻止了多线程并发执行，包含锁的某段代码实际上只能以单线程模式执行，效率就大大地下降了。其次，由于可以存在多个锁，不同的线程持有不同的锁，并试图获取对方持有的锁时，可能会造成死锁，导致多个线程全部挂起，既不能执行，也无法结束，只能靠操作系统强制终止。



#### 4. 死循环

如果你不幸拥有一个多核CPU，你肯定在想，多核应该可以同时执行多个线程。如果写一个死循环的话，会出现什么情况呢？打开任务管理器观察Python进程的CPU使用率。我们可以监控到一个死循环线程会100%占用一个CPU。如果有两个死循环线程，在多核CPU中，可以监控到会占用200%的CPU，也就是占用两个CPU核心。要想把N核CPU的核心全部跑满，就必须启动N个死循环线程。

试试用Python写个死循环：针对IO操作的多线程是有意义的，如果是CPU密集的多线程是没有意义的

```python
import threading, multiprocessing

# 死循环进程
def loop():
    x = 0
    while True:
        x = x ^ 1

# 本机四核CPU, 启四个终端跑这个, Cpu就会100%
# 单独一个终端跑起来, 任务管理器中的python进程CPU占用25%
# 不过由于Python有个GIL, 全局解释器锁，这里说不清，研究的不够hh
for i in range(multiprocessing.cpu_count()):
    t = threading.Thread(target=loop)
    t.start()
```

启动与CPU核心数量相同的N个线程，在4核CPU上可以监控到CPU占用率仅有160%，也就是使用不到两核。

即使启动100个线程，使用率也就170%左右，仍然不到两核。

但是用C、C++或Java来改写相同的死循环，直接可以把全部核心跑满，4核就跑到400%，8核就跑到800%，为什么Python不行呢？

因为Python的线程虽然是真正的线程，但解释器执行代码时，有一个GIL锁：Global Interpreter  Lock，任何Python线程执行前，必须先获得GIL锁，然后，每执行100条字节码，解释器就自动释放GIL锁，让别的线程有机会执行。这个GIL全局锁实际上把所有线程的执行代码都给上了锁，所以，多线程在Python中只能交替执行，即使100个线程跑在100核CPU上，也只能用到1个核。

GIL是Python解释器设计的历史遗留问题，通常我们用的解释器是官方实现的CPython，要真正利用多核，除非重写一个不带GIL的解释器。

所以，在Python中，可以使用多线程，但不要指望能有效利用多核。如果一定要通过多线程利用多核，那只能通过C扩展来实现，不过这样就失去了Python简单易用的特点。

不过，也不用过于担心，Python虽然不能利用多线程实现多核任务，但可以通过多进程实现多核任务。多个Python进程有各自独立的GIL锁，互不影响。



#### 5.小结

多线程编程，模型复杂，容易发生冲突，必须用锁加以隔离，同时，又要小心死锁的发生。

Python解释器由于设计时有GIL全局锁，导致了多线程无法利用多核。多线程的并发在Python中就是一个美丽的梦。



#### 6. threading.local

在多线程环境下，每个线程都有自己的数据。一个线程使用自己的局部变量比使用全局变量好，因为局部变量只有线程自己能看见，不会影响其他线程，而全局变量的修改必须加锁。

但是局部变量也有问题，就是在函数调用的时候，传递起来很麻烦：

```python
def process_student(name):
    std = Student(name)
    # std是局部变量，但是每个函数都要用它，因此必须传进去：
    do_task_1(std)
    do_task_2(std)

def do_task_1(std):
    do_subtask_1(std)
    do_subtask_2(std)

def do_task_2(std):
    do_subtask_2(std)
    do_subtask_2(std)
```

每个函数一层一层调用都这么传参数那还得了？用全局变量？也不行，因为每个线程处理不同的`Student`对象，不能共享。

如果用一个全局`dict`存放所有的`Student`对象，然后以`thread`自身作为`key`获得线程对应的`Student`对象如何？

```python
global_dict = {}

def std_thread(name):
    std = Student(name)
    # 把std放到全局变量global_dict中：
    global_dict[threading.current_thread()] = std
    do_task_1()
    do_task_2()

def do_task_1():
    # 不传入std，而是根据当前线程查找：
    std = global_dict[threading.current_thread()]
    ...

def do_task_2():
    # 任何函数都可以查找出当前线程的std变量：
    std = global_dict[threading.current_thread()]
    ...
```

这种方式理论上是可行的，它最大的优点是消除了`std`对象在每层函数中的传递问题，但是，每个函数获取`std`的代码有点丑。

有没有更简单的方式？

`ThreadLocal`应运而生，不用查找`dict`，`ThreadLocal`帮你自动做这件事：

```python
import threading

# 创建全局ThreadLocal对象:
local_school = threading.local()

def process_student():
    print('Hello, %s (in %s)' % (local_school.student, threading.current_thread().name))

def process_thread(name):
    # 绑定ThreadLocal的student:
    local_school.student = name
    process_student()

if __name__ == '__main__':
    t1 = threading.Thread(target=process_thread, args=('Tom',), name='Thread-A')
    t2 = threading.Thread(target=process_thread, args=('Alex',), name='Thread-B')
    t1.start()
    t2.start()
    t1.join()
    t2.join()
```

执行结果：

```powershell
D:\a\day-day-up\process-and-thread (master -> origin)
λ python 2-5-threading.local.py
Hello, Tom (in Thread-A)
Hello, Alex (in Thread-B)
```

全局变量`local_school`就是一个`ThreadLocal`对象，每个`Thread`对它都可以读写`student`属性，但互不影响。你可以把`local_school`看成全局变量，但每个属性如`local_school.student`都是线程的局部变量，可以任意读写而互不干扰，也不用管理锁的问题，`ThreadLocal`内部会处理。

可以理解为全局变量`local_school`是一个`dict`，不但可以用`local_school.student`，还可以绑定其他变量，如`local_school.teacher`等等。

`ThreadLocal`最常用的地方就是为每个线程绑定一个数据库连接，HTTP请求，用户身份信息等，这样一个线程的所有调用到的处理函数都可以非常方便地访问这些资源。