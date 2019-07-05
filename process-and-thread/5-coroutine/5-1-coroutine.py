def consumer():
    r = ''
    while True:
        print(1)  # 会发现n输出了六次, 第一次是在 send(None)启动生成器, 之后就停在了 n=yield r
        # n = yield r, 1.先接受send的输入, 2.循环再次执行到这里时返回r 循环12

        n = yield r  # 消费者可以通过yield拿到消息

        print(2)  # 会发现2只输出了五次, 因为第一次 send(None)后就停在了上面 n=yield r
        if not n:
            print('这个if不会执行, 因为走不到这里')
            return None
        print('[CONSUMER] Consuming %s...' % n)
        r = '200 OK'  # 处理完下次循环才通过yield返回结果


def produce(c):
    c.send(None)  # 启动生成器
    n = 0
    while n < 5:
        n = n + 1
        print('[PRODUCER] Producing %s...' % n)
        res = c.send(n)  # 一旦生产了东西, 就send切换到消费者去执行, 之后返回结果
        print('[PRODUCER] Consumer return: %s' % res)
    c.close()


if __name__ == '__main__':
    c = consumer()
    produce(c)
