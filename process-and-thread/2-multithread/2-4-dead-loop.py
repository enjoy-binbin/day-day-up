import threading, multiprocessing

# 死循环进程
def loop():
    x = 0
    while True:
        x = x ^ 1


# 本机四核CPU, 启四个终端跑这个, Cpu就会100%
# 单独一个终端跑起来, 任务管理器中的python进程CPU占用25%
# 不过由于Python有个GIL, 全局解释器锁
for i in range(multiprocessing.cpu_count()):
    t = threading.Thread(target=loop)
    t.start()
