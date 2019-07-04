import http.server  # py3中使用http.server替换BaseHTTPServer


class RequestHandler(http.server.BaseHTTPRequestHandler):
    """ Handle HTTP requests by returning a fixed 'page'. """
    # Page to send back.
    Page = '''\
<html>
<body>
<p>Hello, web!</p>
</body>
</html>
'''

    # Handle a GET request.
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(self.Page)))
        self.end_headers()
        self.wfile.write(self.Page.encode())  # py3中需要处理str->bytes
    # 其中do_GET原理如下, self是一个类似Django中的request对象 self.command == 'GET'
    # mname = 'do_' + self.command
    # if not hasattr(self, mname):
    #     self.send_error(
    #         HTTPStatus.NOT_IMPLEMENTED,
    #         "Unsupported method (%r)" % self.command)
    #     return
    # method = getattr(self, mname)
    # method()

if __name__ == '__main__':
    # python server.py
    print('http://127.0.0.1:8080')
    serverAddress = ('', 8080)
    server = http.server.HTTPServer(serverAddress, RequestHandler)
    server.serve_forever()
