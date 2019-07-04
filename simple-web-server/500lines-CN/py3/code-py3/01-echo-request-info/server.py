import http.server


class RequestHandler(http.server.BaseHTTPRequestHandler):
    """ Respond to HTTP requests with info about the request. """

    # Template for page to send back.
    Page = '''\
<html>
<body>
<table>
<tr>  <td>Header</td>         <td>Value</td>          </tr>
<tr>  <td>Date and time</td>  <td>{date_time}</td>    </tr>
<tr>  <td>Client host</td>    <td>{client_host}</td>  </tr>
<tr>  <td>Client port</td>    <td>{client_port}s</td> </tr>
<tr>  <td>Command</td>        <td>{command}</td>      </tr>
<tr>  <td>Path</td>           <td>{path}</td>         </tr>
</table>
</body>
</html>
'''

    # Handle a request by constructing an HTML page that echoes the
    # request back to the caller.
    def do_GET(self):
        # self是一个类似Django中的request对象, self里面包含了很多信息
        page = self.create_page()
        self.send_page(page)

    # Create an information page to send.
    def create_page(self):
        values = {
            'date_time': self.date_time_string(),
            'client_host': self.client_address[0],
            'client_port': self.client_address[1],
            'command': self.command,
            'path': self.path
        }
        page = self.Page.format(**values)
        return page.encode()  # 需要处理下str->bytes

    # Send the created page.
    def send_page(self, page):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", str(len(page)))
        self.end_headers()
        self.wfile.write(page)


if __name__ == '__main__':
    print('http://127.0.0.1:8080')
    serverAddress = ('', 8080)
    server = http.server.HTTPServer(serverAddress, RequestHandler)
    server.serve_forever()
