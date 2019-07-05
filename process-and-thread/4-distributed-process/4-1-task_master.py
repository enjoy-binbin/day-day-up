# task_master.py
import random
from multiprocessing.managers import BaseManager
from multiprocessing import Queue, freeze_support

task_number = 10

# 发送任务的队列:
task_queue = Queue(task_number)
# 接收结果的队列:
result_queue = Queue(task_number)


def get_task():
    return task_queue


def get_result():
    return result_queue


# 从BaseManager继承的QueueManager:
class QueueManager(BaseManager):
    pass


if __name__ == '__main__':
    # freeze_support()

    # 把两个Queue都注册到网络上, callable参数关联了Queue对象:
    QueueManager.register('get_task_queue', callable=get_task)  # win下不能用lambda
    QueueManager.register('get_result_queue', callable=get_result)
    # 绑定端口5000, 设置验证码口令'bin':
    manager = QueueManager(address=('127.0.0.1', 8080), authkey='bin'.encode())
    # 启动Queue:
    manager.start()
    # 获得通过网络访问的Queue对象:
    task = manager.get_task_queue()
    result = manager.get_result_queue()

    # 放几个任务进去:
    for i in range(10):
        n = random.randint(0, 10000)
        print('Put task %d...' % n)
        task.put(n)

    # 从result队列读取结果:
    print('Try get results...')
    for i in range(10):
        r = result.get(timeout=10)  # 从结果队列里获取结果, 超时时间10s
        print('Result: %s' % r)

    # 关闭:
    manager.shutdown()
    print('master exit.')
