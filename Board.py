import random

def main():
	print("Making Board...")
	board = dict()
	make_board(board)
	print()
	print("Making Enemy Board...")
	eboard = dict()
	make_enemy(eboard)
	print()

	check_for_hit(2, 7)
	check_for_hit(1, 3)
	check_for_hit(4, 9)
	check_for_hit(5, 5)

	update_eboard(0,0,0)
	update_eboard(2,5,1)
	update_eboard(6,7,8)

def make_board(board):
	rows = 10
	cols = 10
	board = dict([(0, []), (1, []), (2, []), (3, []), (4, []), (5, []), (6, []), (7, []), (8, []), (9, [])])
	for i in range(0,cols):
		for j in range(0,rows):
			board[i].append("_")
	place_ship(board, "Carrier")
	place_ship(board, "Battleship")	
	place_ship(board, "Cruiser")	
	place_ship(board, "Submarine")
	place_ship(board, "Destroyer")

	print_board(board)
	write_board(board)

def make_enemy(eboard):
	rows = 10
	cols = 10
	board = dict([(0, []), (1, []), (2, []), (3, []), (4, []), (5, []), (6, []), (7, []), (8, []), (9, [])])
	for i in range(0,cols):
		for j in range(0,rows):
			board[i].append("_")
			print(board[i][j], end="")
		print()
	write_eboard(eboard)

def place_ship(board, shipType):
	curX = random.randint(0,9)
	curY = random.randint(0,9)
	orient = random.randint(0,1)
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
				for i in range (0,length):
					if board[curY+i][curX] != "_":
						intersects+=1
				if intersects == 0:
					for k in range(0,length):
						board[curY+k][curX] = title
					placed = 1
					print("Placed " + shipType)
				else:
					curX = random.randint(0,9)
					curY = random.randint(0,9)
			else:
				curX = random.randint(0,9)
				curY = random.randint(0,9)

		if orient == 0:
			if curX + length <= 9:
				for i in range (0,length):
					if board[curY][curX+i] != "_":
						intersects+=1
				if intersects == 0:
					for k in range(0,length):
						board[curY][curX+k] = title
					placed = 1
				else:
					curX = random.randint(0,9)
					curY = random.randint(0,9)
			else:
				curX = random.randint(0,9)
				curY = random.randint(0,9)

def print_board(board):
	for i in range(0,len(board)):
		for j in range(0,len(board[i])):
			print(board[i][j], end="")
		print()

def write_board(board):
	boardFile = open('Boards/player_board.txt', 'w')
	for i in range(0,len(board)):
		for j in range(0,len(board[i])):
			boardFile.write(board[i][j])
		boardFile.write('\n')
	boardFile.close()

def write_eboard(eboard):
	eboardFile = open('Boards\enemy_board.txt', 'w')
	for i in range(0,9):
		for j in range(0,9):
			eboardFile.write("_")
		eboardFile.write('\n')
	eboardFile.close()

def check_for_hit(x, y):
	print("Checking (" + str(y) + ", " + str(x) + ")")
	board = open('Boards\player_board.txt', 'r')
	data = board.read()
	board.close()
	
	rows = data.split('\n')
	if rows[y][x] == "_":
		print("Miss at point (" + str(y) + ", " + str(x) + ")!")
		rows[y][x] = "0"
	elif rows[y][x] == "0" || rows[y][x] == "1" :
		print("This point's been tried already.")
	else:
		print("Hit at point (" + str(y) + ", " + str(x) + ")!")
		check_for_sink(x, y, rows)

def update_eboard(x, y, pwr):
	data = open("Boards\enemy_board.txt", "read")
	eboard = data.read()
	rows = data.split('\n')
	rows[y][x] = pwr
	if pwr == 0:
		print("You missed the enemy at point (" + str(y) +", " + str(x) + ")")
	else:
		print("You hit the enemy at point (" + str(y) +", " + str(x) + ")")


def check_for_sink(x, y, rows):
	title = rows[y][x]
	rows[y][x] = 1
main()