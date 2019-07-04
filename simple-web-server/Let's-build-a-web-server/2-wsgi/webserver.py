# 接着上面的 1-webserver.py
# 如何让服务器可以启动例如 Django-app、Flask-app之类的呢
# 这时候就需要 WSGI(Web Server Gateway Interface)
# Django源码中关于这部分是在 django.core.servers.basehttp中
# 参考文章: https://ruslanspivak.com/lsbaws-part2/

import socket
import sys


class WSGIServer(object):
    address_family = socket.AF_INET  # ipv4
    socket_type = socket.SOCK_STREAM  # Tcp
    request_queue_size = 1  # socket.listen()

    def __init__(self, server_address):
        # Create a listening socket, 创建套接字
        self.listen_socket = listen_socket = socket.socket(self.address_family, self.socket_type)

        # Allow to reuse the same address, 允许复用端口
        listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind, 绑定ip和端口
        listen_socket.bind(server_address)

        # Activate, 启动监听
        listen_socket.listen(self.request_queue_size)

        # Get server host name and port 获取ip地址和端口
        # 返回套接字自己的地址 (addr, port)
        host, port = self.listen_socket.getsockname()
        self.server_name = socket.getfqdn(host)
        self.server_port = port

        # Return headers set by Web framework/Web application
        self.headers_set = []

    def set_app(self, application):
        self.application = application

    def serve_forever(self):
        listen_socket = self.listen_socket
        while True:
            try:
                # New client connection
                self.client_connection, client_address = listen_socket.accept()
                # Handle one request and close the client connection. Then
                # loop over to wait for another client connection
                self.handle_one_request()
            finally:
                listen_socket.close()

    def handle_one_request(self):
        self.request_data = request_data = self.client_connection.recv(1024)
        # Print formatted request data a la 'curl -v'
        print(''.join('< {line}\n'.format(line=line) for line in request_data.splitlines()))

        self.parse_request(request_data)

        # Construct environment dictionary using request data
        env = self.get_environ()

        # It's time to call our application callable and get
        # back a result that will become HTTP response body
        result = self.application(env, self.start_response)

        # Construct a response and send it back to the client
        self.finish_response(result)

    def parse_request(self, text):
        request_line = text.splitlines()[0]
        request_line = request_line.rstrip(b'\r\n')
        # Break down the request line into components
        (self.request_method,  # GET
         self.path,  # /hello
         self.request_version  # HTTP/1.1
         ) = request_line.split()

    def get_environ(self):
        env = dict()
        # The following code snippet does not follow PEP8 conventions
        # but it's formatted the way it is for demonstration purposes
        # to emphasize the required variables and their values
        #
        # Required WSGI variables
        # Web框架使用该字典的信息来指定路由, 请求方法等使用哪个视图
        # 从哪里读取请求主体以及在何处写入错误（如果有的话）。

        #　First, the server starts and loads an ‘application’ callable provided by your Web framework/application
        # Then, the server reads a request
        # Then, the server parses it
        # Then, it builds an ‘environ’ dictionary using the request data
        # Then, it calls the ‘application’ callable with the ‘environ’ dictionary and a ‘start_response’ callable as parameters and gets back a response body.
        # Then, the server constructs an HTTP response using the data returned by the call to the ‘application’ object and the status and response headers set by the ‘start_response’ callable.
        # And finally, the server transmits the HTTP response back to the client
        env['wsgi.version'] = (1, 0)
        env['wsgi.url_scheme'] = 'http'
        env['wsgi.input'] = sys.stdin
        env['wsgi.errors'] = sys.stderr
        env['wsgi.multithread'] = False
        env['wsgi.multiprocess'] = False
        env['wsgi.run_once'] = False
        # Required CGI variables
        env['REQUEST_METHOD'] = self.request_method  # GET
        env['PATH_INFO'] = self.path  # /hello
        env['SERVER_NAME'] = self.server_name  # localhost
        env['SERVER_PORT'] = str(self.server_port)  # 8888
        return env

    def start_response(self, status, response_headers, exc_info=None):
        # Add necessary server headers
        server_headers = [
            ('Date', 'Wes, 3 July 2019 12:42:48 GMT'),
            ('Server', 'WSGIServer 0.2'),
        ]
        self.headers_set = [status, response_headers + server_headers]
        # To adhere to WSGI specification the start_response must return
        # a 'write' callable. We simplicity's sake we'll ignore that detail
        # for now.
        # return self.finish_response

    def finish_response(self, result):
        try:
            status, response_headers = self.headers_set
            response = 'HTTP/1.1 {status}\r\n'.format(status=status)
            for header in response_headers:
                response += '{0}: {1}\r\n'.format(*header)
            response += '\r\n'
            for data in result:
                response += data
            # Print formatted response data a la 'curl -v'
            print(''.join(
                '> {line}\n'.format(line=line)
                for line in response.splitlines()
            ))
            self.client_connection.sendall(response.encode('utf-8'))
        finally:
            self.client_connection.close()


SERVER_ADDRESS = (HOST, PORT) = '', 8888


def make_server(server_address, application):
    server = WSGIServer(server_address)
    server.set_app(application)
    return server


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('Provide a WSGI application object as module:callable')
    app_path = sys.argv[1]
    module, application = app_path.split(':')
    module = __import__(module)
    application = getattr(module, application)
    httpd = make_server(SERVER_ADDRESS, application)
    print('WSGIServer: Serving HTTP on port {port} ...\n'.format(port=PORT))
    httpd.serve_forever()
    # python python webserver.py app:simple_app
    # python python webserver.py app:application
    # ctrl + c 停止刷新浏览器
