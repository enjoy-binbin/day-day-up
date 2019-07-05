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

    pool = Pool()
    for i in range(5):  # 创建5个进程，因为当前电脑是四核CPU，所以会有个进程会等待，看后面的结果
        pool.apply(long_time_task, args=(i,))

    print('Waiting for all subprocesses done...')
    pool.close()  # 对pool调用close后之后就不能再添加新的进程
    pool.join()  # 对pool调用join前必须先close, 会等待所有子进程完成
    print('All subprocesses done.')

    print('Total time %0.2f seconds' % (time.time() - start))
