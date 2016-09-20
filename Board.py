# Jason Sanders & Bradley White
# CSCI 466: Networks
# Battleship HTTP: Board
# September 19, 2016
#
# This python module handles creation, updating of both boards, and external files
# related to each board. The ships are placed randomly on the board each time the server
# is started.
#Something

import random

# Global Variables
# own_board
board = dict([(0, []), (1, []), (2, []), (3, []), (4, []), (5, []), (6, []), (7, []), (8, []), (9, [])])
# opponent_board
eboard = dict([(0, []), (1, []), (2, []), (3, []), (4, []), (5, []), (6, []), (7, []), (8, []), (9, [])])
# hit counters for each ship to check if sunk
counters = [0, 0, 0, 0, 0]


# Invoked by the server to create new boards
def main():
    global board
    global eboard

    print("Making Board...")
    make_board()
    print()

    print("Making Enemy Board...")
    make_opponent()
    print()


# Create own_board
def make_board():
    global board

    # Start by making every location "water"
    for i in range(0, len(board)):
        for j in range(0, 10):
            board[i].append("_")

    # Call helper functions to place each ship
    place_ship("Carrier")
    place_ship("Battleship")
    place_ship("Cruiser")
    place_ship("Submarine")
    place_ship("Destroyer")

    # Call helper functions to print the board to the terminal and write the txt and HTML files
    print_board()
    write_board()


# Places a ship on the board randomly
def place_ship(shipType):
    global board

    # Get random starting coordinates and a random orientation
    curX = random.randint(0, 9)
    curY = random.randint(0, 9)
    orient = random.randint(0, 1)
    placed = 0

    # Parameters for each type of ship
    if shipType == "Carrier":
        length = 5
        title = "C"
    elif shipType == "Battleship":
        length = 4
        title = "B"
    elif shipType == "Cruiser":
        length = 3
        title = "R"
    elif shipType == "Destroyer":
        length = 2
        title = "D"
    elif shipType == "Submarine":
        length = 3
        title = "S"
    else:
        print("Tried to place invalid ship type.")

    # Loop until the ship is placed
    while placed == 0:
        intersects = 0

        # Ship is being placed vertically
        if orient == 1:
            # Make sure the ship will fit on the board
            if curY + length <= 9:
                # Make sure the ship won't cross over another ship
                for i in range(0, length):
                    if board[curY + i][curX] != "_":
                        intersects += 1
                # If we are past the checks, place the ship
                if intersects == 0:
                    for k in range(0, length):
                        board[curY + k][curX] = title
                    placed = 1
                # Otherwise the checks failed, get new starting coordinates and start over
                else:
                    curX = random.randint(0, 9)
                    curY = random.randint(0, 9)
            else:
                curX = random.randint(0, 9)
                curY = random.randint(0, 9)

        # Ship is being placed horizontally using the same logic as above
        if orient == 0:
            if curX + length <= 9:
                for i in range(0, length):
                    if board[curY][curX + i] != "_":
                        intersects += 1
                if intersects == 0:
                    for k in range(0, length):
                        board[curY][curX + k] = title
                    placed = 1
                else:
                    curX = random.randint(0, 9)
                    curY = random.randint(0, 9)
            else:
                curX = random.randint(0, 9)
                curY = random.randint(0, 9)


# Print own_board to the terminal
def print_board():
    global board

    for i in range(0, len(board)):
        for j in range(0, len(board[i])):
            print(board[i][j], end="")
        print()


# Write own_board to txt and html files
def write_board():
    global board

    boardFile = open('own_board.txt', 'w')
    for i in range(0, len(board)):
        for j in range(0, len(board[i])):
            boardFile.write(board[i][j])
        boardFile.write('\n')
    boardFile.close()

    boardPage = open('own_board.html', 'w')
    for i in range(0, len(board)):
        boardPage.write(str(board[i]))
        boardPage.write('</br>')
    boardPage.close()


# Check if a coordinate has been used from a previous fire message, used for 410 error by the server
def useCoord(coord):
    global board

    if board[coord[1]][coord[0]] is "1" or board[coord[1]][coord[0]] is "0":
        return True
    else:
        return False


# Create opponent_board, all locations are "water" initially
def make_opponent():
    global eboard

    for i in range(0, len(eboard)):
        for j in range(0, 10):
            eboard[i].append("_")

    # Call helper functions
    # print_opponent()
    write_opponent()


# Print opponent_board to terminal
def print_opponent():
    global eboard

    for i in range(0, len(eboard)):
        for j in range(0, len(eboard[i])):
            print(eboard[i][j], end="")
        print()


# Write opponent_board to txt and html files
def write_opponent():
    global eboard

    eboardFile = open('opponent_board.txt', "w")
    for i in range(0, len(eboard)):
        for j in range(0, len(eboard[i])):
            eboardFile.write(eboard[i][j])
        eboardFile.write('\n')
    eboardFile.close()

    htmlFile = open("opponent_board.html", "w")
    for i in range(0, len(eboard)):
        htmlFile.write(str(eboard[i]))
        htmlFile.write('</br>')
    htmlFile.close()


# Updates the opponent_board txt and html files which are then used by each call of the client
# because clients are not persistent
def update_eboard(coord, result):
    # Open the file for reading
    filename = 'opponent_board.txt'
    file = open(filename, "r")
    # Create a new dictionary and fill it with the characters in the file, line by line
    eboard = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: []}
    j = 0
    for line in file:
        charList = list(line)
        for i in range(0, len(charList)):
            if charList[i] is not "\n":
                eboard[j].append(charList[i])
        j += 1
    file.close()
    # Update the required character from the fire message within the dictionary
    if result is "0":
        eboard[coord[1]][coord[0]] = "0"
    elif result is "1":
        eboard[coord[1]][coord[0]] = "1"

    # Open the file again and write the updated dictionary to it
    eboardFile = open(filename, "w")
    for i in range(0, len(eboard)):
        for j in range(0, len(eboard[i])):
            eboardFile.write(eboard[i][j])
        eboardFile.write('\n')
    eboardFile.close()

    # Write the data with proper formatting to the html file
    htmlFile = open("opponent_board.html", "w")
    for i in range(0, len(eboard)):
        htmlFile.write(str(eboard[i]))
        htmlFile.write('</br>')
    htmlFile.close()


# Check if a ship was hit from a fire message
def check_for_hit(coord):
    global board
    global counters

    # If the coordinate was water, update it to a 0 and return miss
    if board[coord[1]][coord[0]] == "_":
        board[coord[1]][coord[0]] = "0"
        write_board()
        return (("0"))
    # Otherwise there was a ship hit
    else:
        # Parse the character in the coordinate and figure out the ship hit, update the counter for how many
        # Hits the ship has received
        title = board[coord[1]][coord[0]]
        if title is "C":
            # print(title)
            counters[0] += 1
        elif title is "B":
            # print(title)
            counters[1] += 1
        elif title is "R":
            # print(title)
            counters[2] += 1
        elif title is "S":
            # print(title)
            counters[3] += 1
        elif title is "D":
            # print(title)
            counters[4] += 1
        else:
            print("You hit a ghost ship...")
        # Call helper function to check if the ship is sunk, and return the result.
        # Also updates the coordinate to a 1 for hit.
        return check_for_sink(coord, title)


# Check if a ship has been sunk and update a coordinate to hit
def check_for_sink(coord, title):
    global board
    global counters

    # Update the coordinate to hit
    board[coord[1]][coord[0]] = "1"
    # Call helper function to update the board
    write_board()

    # Check if a ship's counter is equal to it's length if so return a sink
    if counters[0] == 5:
        # print("There's a sunken Carrier!")
        return (1, "C")
    elif counters[1] == 4:
        # print("There's a sunken Battleship!")
        return (1, "B")
    elif counters[2] == 3:
        # print("There's a sunken Cruiser!")
        return (1, "R")
    elif counters[3] == 3:
        # print("There's a sunken Submarine!")
        return (1, "S")
    elif counters[4] == 2:
        # print("There's a sunken Destroyer!")
        return (1, "D")
    # Otherwise return a hit only
    else:
        # print("No sink!")
        return (('1'))
