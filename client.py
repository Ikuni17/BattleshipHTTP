import argparse
import urllib.parse
import http.client
import time

# Parse command line arguments for server IP, port and fire coordinates
def parseArgs():
    # Start a new argument parser
    parser = argparse.ArgumentParser()

    # Add the four arguments
    parser.add_argument("ip")
    parser.add_argument("port", type=int)
    parser.add_argument("x_coordinate", type=int)
    parser.add_argument("y_coordinate", type=int)
    args = parser.parse_args()

    # Save the arguments into new variables
    server_address = args.ip
    port = args.port
    coordinates = (args.x_coordinate, args.y_coordinate)
    # print(server_address)
    # print(port)
    # print(coordinates)
    return (server_address, port, coordinates)


def openConnection(arguments):
    # Create a TCP/IP socket
    # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port on which the server is listening
    server_address = (arguments[0], arguments[1])
    connection = http.client.HTTPConnection(arguments[0], arguments[1])
    print('Connecting to IP: {} on port: {}'.format(*server_address))
    # sock.connect(server_address)

    #url = 'http://' + arguments[0] + ':' + str(arguments[1])
    #parsed = urllib.parse.urlsplit(url)
    #url = urllib.parse.urlunsplit(parsed)

    params = urllib.parse.urlencode({'x': arguments[2][0], 'y': arguments[2][1]})
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    connection.request("POST", "", params, headers)
    r2 = connection.getresponse()
    print(r2.status, r2.reason)
    connection.close()
    return r2.reason
    # msg2 = msg.split('&')
    # print(msg2)
    # connection.request('GET', '/')
    # r1 = connection.getresponse()
    # print(r1.status, r1.reason)

    # sock.close()

def forwardMessage(arguments, msg):
    coord = (arguments[2][0], arguments[2][1])
    homeServer = ('127.0.0.1', arguments[1])
    #homeServer = (arguments[0], arguments[1])
    homeConnection = http.client.HTTPConnection('localhost', arguments[1])
    print('Connecting to IP: {} on port: {}'.format(*homeServer))

    params = urllib.parse.urlencode({'x': coord[0], 'y': coord[1], 'hit':msg})
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    homeConnection.request("POST", "", params, headers)
    r3 = homeConnection.getresponse()
    print(r3.status, r3.reason)
    homeConnection.close()

def main():
    arguments = parseArgs()
    msg = openConnection(arguments)
    forwardMessage(arguments, msg)

main()
