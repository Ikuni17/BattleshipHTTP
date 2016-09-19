import random

# Global Variables
board = dict([(0, []), (1, []), (2, []), (3, []), (4, []), (5, []), (6, []), (7, []), (8, []), (9, [])])
eboard = dict([(0, []), (1, []), (2, []), (3, []), (4, []), (5, []), (6, []), (7, []), (8, []), (9, [])])
counters = [0, 0, 0, 0, 0]


def main():
    global board
    global eboard

    print("Making Board...")
    make_board()
    print()

    print("Making Enemy Board...")
    make_opponent()
    print()


def make_board():
    global board

    for i in range(0, len(board)):
        for j in range(0, 10):
            board[i].append("_")

    place_ship("Carrier")
    place_ship("Battleship")
    place_ship("Cruiser")
    place_ship("Submarine")
    place_ship("Destroyer")

    print_board()
    write_board()


def place_ship(shipType):
    global board

    curX = random.randint(0, 9)
    curY = random.randint(0, 9)
    orient = random.randint(0, 1)
    placed = 0

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

    while placed == 0:
        intersects = 0

        if orient == 1:
            if curY + length <= 9:
                for i in range(0, length):
                    if board[curY + i][curX] != "_":
                        intersects += 1
                if intersects == 0:
                    for k in range(0, length):
                        board[curY + k][curX] = title
                    placed = 1
                else:
                    curX = random.randint(0, 9)
                    curY = random.randint(0, 9)
            else:
                curX = random.randint(0, 9)
                curY = random.randint(0, 9)

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


def print_board():
    global board

    for i in range(0, len(board)):
        for j in range(0, len(board[i])):
            print(board[i][j], end="")
        print()


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
        boardPage.write(board[i])
        boardPage.write('</br>')
    boardPage.close()


def useCoord(coord):
    global board

    if board[coord[1]][coord[0]] is "1" or board[coord[1]][coord[0]] is "0":
        return True
    else:
        return False


def make_opponent():
    global eboard

    for i in range(0, len(eboard)):
        for j in range(0, 10):
            eboard[i].append("_")

    # print_opponent()
    write_opponent()


def print_opponent():
    global eboard

    for i in range(0, len(eboard)):
        for j in range(0, len(eboard[i])):
            print(eboard[i][j], end="")
        print()


def write_opponent():
    global eboard

    eboardFile = open('opponent_board.txt', "w")
    for i in range(0, len(eboard)):
        for j in range(0, len(eboard[i])):
            eboardFile.write(eboard[i][j])
        eboardFile.write('\n')
    eboardFile.close()


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
    # Update the required character within the dictionary
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

    # Write the data with proper formatting to an html file
    htmlFile = open("opponent_board.html", "w")
    for i in range(0,len(eboard)):
        htmlFile.write(str(eboard[i]))
        htmlFile.write('</br>')
    htmlFile.close()



def check_for_hit(coord):
    global board
    global counters

    if board[coord[1]][coord[0]] == "_":
        board[coord[1]][coord[0]] = "0"
        write_board()
        return (("0"))
    else:
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
        return check_for_sink(coord, title)


def check_for_sink(coord, title):
    global board
    global counters

    board[coord[1]][coord[0]] = "1"
    write_board()

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
    else:
        # print("No sink!")
        return (('1'))
