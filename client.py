# Jason Sanders & Bradley White
# CSCI 466: Networks
# Battleship HTTP: Client
# September 19, 2016
#
# This python module sends fire messages as POST requests to play Battleship over HTTP
# The program takes four arguments and should be invoked every time a fire message needs to be sent:
# server IP address, server port, x_coordinate, y_coordinate

import argparse
import urllib.parse
import http.client
import Board


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
    return (server_address, port, coordinates)

# Opens connection with the server and sends a fire message as a POST request
def openConnection(arguments):
    # Connect to the server at the IP and the port specified
    server_address = (arguments[0], arguments[1])
    connection = http.client.HTTPConnection(arguments[0], arguments[1])
    print('Connecting to IP: {} on port: {}'.format(*server_address))

    # Parse the coordinates into a proper POST request
    params = urllib.parse.urlencode({'x': arguments[2][0], 'y': arguments[2][1]})
    # Create the header
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    # Send the POST request with parameters and header to the server
    connection.request("POST", "", params, headers)
    # Wait for the response
    r2 = connection.getresponse()
    # Print the status code and message or type of error to terminal
    print(r2.status, r2.reason)
    # Close the connection
    connection.close()
    # If the fire message was legitimate, updated the opponent_board with the results
    if r2.status is 200:
        coord = (arguments[2][0], arguments[2][1])
        # Split the message into a list
        msg2 = r2.reason.split('=')
        # Send the coordinates and a 1 or 0 for hit or miss to Board for updates
        Board.update_eboard(coord, msg2[1])

# Invokes the other functions
def main():
    # Pass terminal arguments for opening the connection
    arguments = parseArgs()
    openConnection(arguments)

# Start!
main()
