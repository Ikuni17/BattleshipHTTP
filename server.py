# Jason Sanders & Bradley White
# CSCI 466: Networks
# Battleship HTTP: Server
# September 19, 2016
#
# This python module handles creation of a HTTP server and handling incoming requests
# The program takes two arguments: port number and location of own_board.txt
# The status of the boards can be checked from a browser at:
# http://localhost:port/own_board.html and http://localhost:port/opponent_board.html

import socket
import argparse
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import Board
from os import curdir, sep

# Global variables
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
    return port


# Handles requests from clients
class requestHandler(BaseHTTPRequestHandler):
    global boardLocation

    # Send header information
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    # Send various GET requests
    def do_GET(self):
        # Open html file representing own board in browser
        if self.path == '/own_board.html':
            # Open the file in the server directory
            f = open(curdir + sep + self.path)
            # Send OK response and headers
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            # Write the file to the browser then close it
            self.wfile.write(bytes(f.read(), 'utf-8'))
            f.close()
            return
        # Open html file representing opponent board in browser
        elif self.path == '/opponent_board.html':
            # Open the file in the server directory
            f = open(curdir + sep + self.path)
            # Send OK response and headers
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            # Write the file to the browser then close it
            self.wfile.write(bytes(f.read(), 'utf-8'))
            f.close()
            return

    # Handle POST requests from clients
    def do_POST(self):
        length = int(self.headers['Content-Length'])
        # Parse the POST data from the url query
        post_data = urllib.parse.parse_qs(self.rfile.read(length).decode('utf-8'))
        # Test if the X and Y coordinates are actually integers, if not respond with a 400 error (Bad Request)
        try:
            coord = (int(post_data['x'][0]), int(post_data['y'][0]))
        except ValueError:
            self.send_error(400)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            return
        # Since we have integer coordinates now, check that they are within the bounds of the board, if not
        # respond with a 404 error (Not Found)
        for i in range(0, len(coord)):
            if coord[i] < 0 or coord[i] > 9:
                self.send_error(404)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                return
        # Have Board check that the coordinates have not been used in a fire message previously, if so
        # respond with 410 error (Gone)
        if (Board.useCoord(coord)):
            self.send_error(410)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            return

        # If the fire message reaches this point, we know it's a good coordinate so have the Board check if it
        # is a hit or miss and possibly a sink. message is formatted hit=1/0&sunk=C/D/..., with sunk being optional
        message = Board.check_for_hit(coord)
        # If there is no sink information, pass a response with hit or miss
        if len(message) is 1:
            answer = ('hit=' + str(message[0]))
        # Otherwise there is sink information to include
        if len(message) is 2:
            answer = ('hit=' + str(message[0]) + '&' + 'sunk=' + str(message[1]))
        # Send ok response with the correct answer
        self.send_response(200, answer)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        return


# Called to setup and start the server
def openServer(port):
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Get the IP of the server, and use the port specified from arguments
    serverAddress = (socket.gethostbyname(socket.gethostname()), port)
    # Print the information
    print('Starting server on IP: {} and port: {}'.format(*serverAddress))
    # Create a new request handler (server) at the address
    server = HTTPServer(serverAddress, requestHandler)
    # Use HTTP 1.1, causes the server to lock up currently
    # requestHandler.protocol_version = "HTTP/1.1"

    # Listen for connections forever unless CTRL + C is received in command prompt
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()
    print('Server closed')


# Start!
def main():
    # Call main() in Board to handle setup of boards and external files
    Board.main()
    # Save the port and pass it for opening the server
    port = parseArgs()
    openServer(port)


main()
