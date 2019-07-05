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
