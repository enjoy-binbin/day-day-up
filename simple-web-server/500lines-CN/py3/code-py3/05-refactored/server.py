import os
import http.server
import subprocess


class ServerException(Exception):
    """ For internal error reporting. """
    pass


class BaseCase(object):
    """ Parent for case handlers. """

    def index_path(self, handler):
        return os.path.join(handler.full_path, 'index.html')

    def handle_file(self, handler, full_path):
        try:
            with open(full_path, 'rb') as reader:
                content = reader.read()
            handler.send_content(content)
        except IOError as msg:
            msg = "'{0}' cannot be read: {1}".format(handler.path, msg)
            handler.handle_error(msg)

    def test(self, handler):
        # assert(False, 'test function not implemented.') won't work
        # Because bool((False, 'test function not implemented.')) == True
        assert False, 'test function not implemented.'

    def act(self, handler):
        assert False, 'act function not implemented.'


class CaseNoFile(BaseCase):
    """ File or directory does not exist. """

    def test(self, handler):
        return not os.path.exists(handler.full_path)

    def act(self, handler):
        raise ServerException("'{0}' not found".format(handler.path))


class CaseCgiFile(BaseCase):
    """ Something runnable. """

    def run_cgi(self, handler):
        cmd = "python " + handler.full_path
        # os.popen2在py3中废弃了, 使用subprocess
        # status, output = subprocess.getstatusoutput(cmd)  # status执行成功是返回的0
        output = subprocess.getoutput(cmd)
        handler.send_content(output.encode())

    def test(self, handler):
        return os.path.isfile(handler.full_path) and \
               handler.full_path.endswith('.py')

    def act(self, handler):
        self.run_cgi(handler)


class CaseExistingFile(BaseCase):
    """ File exists. """

    def test(self, handler):
        return os.path.isfile(handler.full_path)

    def act(self, handler):
        self.handle_file(handler, handler.full_path)


class CaseDirectoryIndexFile(BaseCase):
    """ Serve index.html page for a directory. """

    def test(self, handler):
        return os.path.isdir(handler.full_path) and \
               os.path.isfile(self.index_path(handler))

    def act(self, handler):
        self.handle_file(handler, self.index_path(handler))


class CaseDirectoryNoIndexFile(BaseCase):
    """ Serve listing for a directory without an index.html page. """
    Listing_Page = '''\
        <html>
        <body>
        <ul>
        {0}
        </ul>
        </body>
        </html>
        '''

    def list_dir(self, handler):
        try:
            entries = os.listdir(handler.full_path)
            bullets = ['<li>{0}</li>'.format(e)
                       for e in entries if not e.startswith('.')]
            page = self.Listing_Page.format('\n'.join(bullets))
            handler.send_content(page.encode())  # 继续py3处理str->bytes
        except OSError as msg:
            msg = "'{0}' cannot be listed: {1}".format(handler.path, msg)
            handler.handle_error(msg)

    def test(self, handler):
        return os.path.isdir(handler.full_path) and \
               not os.path.isfile(self.index_path(handler))

    def act(self, handler):
        self.list_dir(handler)


class CaseAlwaysFail(BaseCase):
    """ Base case if nothing else worked. """

    def test(self, handler):
        return True

    def act(self, handler):
        raise ServerException("Unknown object '{0}'".format(handler.path))


class RequestHandler(http.server.BaseHTTPRequestHandler):
    """
    If the requested path maps to a file, that file is served.
    If anything goes wrong, an error page is constructed.
    """

    Cases = [CaseNoFile, CaseCgiFile, CaseExistingFile, CaseDirectoryIndexFile, CaseDirectoryNoIndexFile,
             CaseAlwaysFail]

    # How to display an error.
    Error_Page = """\
    <html>
    <body>
    <h1>Error accessing {path}</h1>
    <p>{msg}</p>
    </body>
    </html>
    """

    # Classify and handle request.
    def do_GET(self):
        try:

            # Figure out what exactly is being requested.
            self.full_path = os.getcwd() + self.path

            # Figure out how to handle it.
            for case in self.Cases:
                cls = case()
                if cls.test(self):
                    cls.act(self)
                    break

        # Handle errors.
        except Exception as msg:
            self.handle_error(msg)

    # Handle unknown objects.
    def handle_error(self, msg):
        content = self.Error_Page.format(path=self.path, msg=msg)
        self.send_content(content.encode(), 404)

    # Send actual content.
    def send_content(self, content, status=200):
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)


if __name__ == '__main__':
    print('http://127.0.0.1:8080')
    serverAddress = ('', 8080)
    server = http.server.HTTPServer(serverAddress, RequestHandler)
    server.serve_forever()
