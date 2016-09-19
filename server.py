import socket
import argparse
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import logging
import Board

boardLocation = ""

# Parse command line arguments for port number and board location
def parseArgs():
    global boardLocation
    # Start a new argument parser
    parser = argparse.ArgumentParser()

    # Add the two arguments
    parser.add_argument("port", type=int)
    parser.add_argument("file_name")
    args = parser.parse_args()

    # Save the arguments into new variables
    port = args.port
    boardLocation = args.file_name
    file = open(boardLocation, "r")
    file.close()
    return port


class requestHandler(BaseHTTPRequestHandler):
    global boardLocation

    def do_HEAD(self):
        #logging.debug('HEADER %s' % (self.path))
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def info(self):
        self.wfile.write('<html>'.encode('utf-8'))
        self.wfile.write('  <head>'.encode('utf-8'))
        self.wfile.write('    <title>Server Info</title>'.encode('utf-8'))
        self.wfile.write('  </head>'.encode('utf-8'))
        self.wfile.write('  <body>'.encode('utf-8'))
        self.wfile.write('    <table>'.encode('utf-8'))
        self.wfile.write('      <tbody>'.encode('utf-8'))
        self.wfile.write('        <tr>'.encode('utf-8'))
        self.wfile.write('          <td>client_address</td>'.encode('utf-8'))
        self.wfile.write('          <td>%r</td>'.encode('utf-8') % (repr(self.client_address)))
        self.wfile.write('        </tr>'.encode('utf-8'))
        self.wfile.write('        <tr>'.encode('utf-8'))
        self.wfile.write('          <td>command</td>'.encode('utf-8'))
        self.wfile.write('          <td>%r</td>'.encode('utf-8') % (repr(self.command)))
        self.wfile.write('        </tr>'.encode('utf-8'))
        self.wfile.write('        <tr>'.encode('utf-8'))
        self.wfile.write('          <td>headers</td>'.encode('utf-8'))
        self.wfile.write('          <td>%r</td>'.encode('utf-8') % (repr(self.headers)))
        self.wfile.write('        </tr>'.encode('utf-8'))
        self.wfile.write('        <tr>'.encode('utf-8'))
        self.wfile.write('          <td>path</td>'.encode('utf-8'))
        self.wfile.write('          <td>%r</td>'.encode('utf-8') % (repr(self.path)))
        self.wfile.write('        </tr>'.encode('utf-8'))
        self.wfile.write('        <tr>'.encode('utf-8'))
        self.wfile.write('          <td>server_version</td>'.encode('utf-8'))
        self.wfile.write('          <td>%r</td>'.encode('utf-8') % (repr(self.protocol_version)))
        self.wfile.write('        </tr>'.encode('utf-8'))
        self.wfile.write('        <tr>'.encode('utf-8'))
        self.wfile.write('          <td>sys_version</td>'.encode('utf-8'))
        self.wfile.write('          <td>%r</td>'.encode('utf-8') % (repr(self.sys_version)))
        self.wfile.write('        </tr>'.encode('utf-8'))
        self.wfile.write('      </tbody>'.encode('utf-8'))
        self.wfile.write('    </table>'.encode('utf-8'))
        self.wfile.write('  </body>'.encode('utf-8'))
        self.wfile.write('</html>'.encode('utf-8'))
        self.send_response(200)  # OK
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        return

    def do_GET(self):
        if self.path == '/info' or self.path == '/info/':
            self.send_response(200)  # OK
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.info()
            return
        elif self.path == '/own_board.html':
            self.send_response(200)  # OK
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            #file = urllib.urlopen('http://192.168.1.10:5000/own_board.txt').read()
            '''file = open('own_board.txt','rb')
            #self.wfile.write(bytes(file.read(),'utf-8'))
            for line in file:
                self.wfile.write(line)
                self.wfile.write(bytes('\n','utf-8'))
            file.close()'''
            return
        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes("Hello World!", 'utf-8'))
            return

        '''elif self.path == '/own_board.html':
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write('<html>'.encode('utf-8'))
                    self.wfile.write('  <head>'.encode('utf-8'))
                    self.wfile.write('    <title>Server Info</title>'.encode('utf-8'))
                    self.wfile.write('  </head>'.encode('utf-8'))
                    self.wfile.write('  <body>'.encode('utf-8'))
                    self.wfile.write('      <a href=file://///localhost/own_board.txt>own_board.text</a>'.encode('utf-8'))
                    self.wfile.write('  </body>'.encode('utf-8'))
                    self.wfile.write('</html>'.encode('utf-8'))'''
    def do_POST(self):
        length = int(self.headers['Content-Length'])
        post_data = urllib.parse.parse_qs(self.rfile.read(length).decode('utf-8'))
        try:
            coord = (int(post_data['x'][0]), int(post_data['y'][0]))
        except ValueError:
            self.send_error(400)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            return
        for i in range(0, len(coord)):
            if coord[i] < 0 or coord[i] > 9:
                self.send_error(404)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                return
        if (Board.useCoord(coord)):
            self.send_error(410)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            return

        message = Board.check_for_hit(coord)
        if len(message) is 1:
            answer = ('hit=' + str(message[0]))
        if len(message) is 2:
            answer = ('hit=' + str(message[0]) + '&' + 'sunk=' + str(message[1]))
        self.send_response(200, answer)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        return


def openServer(port):
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    serverAddress = (socket.gethostbyname(socket.gethostname()), port)
    print('Starting server on IP: {} and port: {}'.format(*serverAddress))
    server = HTTPServer(serverAddress, requestHandler)
    #requestHandler.protocol_version = "HTTP/1.1"

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()
    print('Server closed')


def main():
    Board.main()
    port = parseArgs()
    openServer(port)


main()
