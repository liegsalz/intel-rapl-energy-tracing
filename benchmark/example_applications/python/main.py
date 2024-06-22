from http.server import HTTPServer, SimpleHTTPRequestHandler

server_address = ('', 8000)

class MyRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Content-Type', 'text/html')
        super().end_headers()

httpd = HTTPServer(server_address, MyRequestHandler)

print('Server running on http://localhost:8000')
httpd.serve_forever()