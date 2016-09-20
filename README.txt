The following will explain how to play Battleship using our server:

To begin, you'll need to open a command window and navigate to the folder that holds the files.

To open the server, type "(python.exe address) server.py (port you'd like to use) own_board.txt"

For example, a server opened from a user using Python 3.4 on port 5000 might need this command:

"C:\Python34\python.exe server.py 5000 own_board.txt"

Open a second command window in the same location. Make sure your opponent has his server running, and then type:

"(python.exe address) client.py (IP of your opponent) (Port of your opponent) x y"

For example, a fire from a user with Python 3.4 at location (2,4) to a server on port 5001 with an IP of 8.8.8.8 might be written as:

C:\Python34\python.exe client.py 8.8.8.8 5001 2 4

into the command line in order to fire at the coordinates x and y.

If your coordinates are valid and haven't been used yet, the server will return 200, then a hit=0 for a miss or hit=1 for a hit.

In the event of a sink, the server will return 200, then hit=1&sink=C/B/R/S/D where the character after "sink=" represents the ship that was sunk:
	
	C = Carrier
	B = Battleship
	R = Cruiser
	S = Submarine
	D = Destoryer

If the coordinates are invalid, the server will return a 404 or a 400.

If the coordinates have been used, the server will return a 410.
