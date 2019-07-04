import socket


# 1. The server creates a TCP/IP socket. This is done with the following statement in Python:
# listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2. The server might set some socket options (this is optional, but you can see that the server code above does just that to be able to re-use the same address over and over again if you decide to kill and re-start the server right away).
# listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# 3. Then, the server binds the address. The bind function assigns a local protocol address to the socket. With TCP, calling bind lets you specify a port number, an IP address, both, or neither.1
# listen_socket.bind(SERVER_ADDRESS)

# 4. Then, the server makes the socket a listening socket
# listen_socket.listen(REQUEST_QUEUE_SIZE)


# 一个简单的通过socket编程实现Web服务的例子
# 逻辑很简单, 创建套接字监听本地8000端口, 接收客户端, 返回HTTP相应
# And how to run a app like django app? Go and see the part2- wsgi
def main():
    HOST, PORT = '127.0.0.1', 8080

    # https://www.runoob.com/python/python-socket.html
    # 1. 建立socket套接字, AF_INET: ipv4, SOCK_STREAM: TCP
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 2. s.setsockopt(level,optname,value)设置给定套接字选项的
    # 设置端口可复用, ctrl + c后可以快速重启
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # 3. 绑定ip和端口
    listen_socket.bind((HOST, PORT))

    # 4. 设置backlog-socket 连接最大排队数量
    listen_socket.listen(1)

    print('Serving HTTP on port %s ...' % PORT)
    print('%s:%s' % (HOST, PORT))

    while True:
        # accept()被动接受TCP客户端连接,(阻塞式)等待连接的到来
        client_connection, client_address = listen_socket.accept()
        request = client_connection.recv(1024)
        print(request.decode('utf-8'))

        http_response = b"""\
    HTTP/1.1 200 OK

    Hello, World ! from simple-web-server
    """
        client_connection.sendall(http_response)
        client_connection.close()  # 关闭套接字


if __name__ == '__main__':
    print('http://127.0.0.1:8080')
    main()
