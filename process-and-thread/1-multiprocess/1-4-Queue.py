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
