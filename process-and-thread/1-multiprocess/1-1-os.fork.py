# coding: utf-8
# 需要运行在linux下

import os

print('Process (%s) start ...' % os.getpid())

pid = os.fork()

if pid == 0:
    print('i am a child proccess (%s) and my parent is (%s)' % (os.getpid(), os.getppid()))
else:
    print('i (%s) just created a child process (%s)' % (os.getpid(), pid))

# 输出结果
# [root@localhost ~]# python multiprocessing.py 
# Process (6576) start ...
# i (6576) just created a child process (6577)
# i am a child proccess (6577) and my parent is (6576)
# [root@localhost ~]#
