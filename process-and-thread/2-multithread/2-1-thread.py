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
