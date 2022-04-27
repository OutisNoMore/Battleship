"""Object for the player and the computer

  The PlayerBoard represents a players ships, and a 2D array
  to keep track of hits, misses, and ship placements. The ComputerBoard
  inherits the PlayerBoard class, and represents an AI enemy. It will
  randomly place boats, and will use an algorithm to make slightly less
  random attacks.
"""
from util import Error, Flag
from ship import Ship
import random
import json

class PlayerBoard:
    """Represents a player

    A battleship player has a board, and a list of
    ships. They can make moves, place ships, among other
    functions.

    Attributes:
    __________
      _board: 2D list of string symbols for battleship board
      _ships: List of all ships
      _currentShip: current ship to place
    """
    def __init__(self):
        """Creates a PlayerBoard

        Create a PlayerBoard that represents the player.
        A list of ships, and the player's board is stored as
        a 2D list of char.

        Parameters:
        ___________
          None

        Return:
        _______
          None
        """
        self._board = list()  # 2D List of characters for Board
        self._ships = list()  # List of all ships
        self._currentShip = 0 # Index of the current ship
        self._initializeBoard(10, 10) # Create a 10x10 board

    def _initializeBoard(self, width, height):
        """Initialize the board with characters

        Creates a board of given dimensions, and initializes with
        character 'E', to indicate empty.

        Parameters:
        ___________
          width: Width of board to create
          height: Height of board to create

        Return:
        _______
          None
        """
        for i in range(0, width):
            self._board.append([]) # Make a 2D
            for j in range(0, height):
                self._board[i].append('E') # add 'E' for empty

    def initFleet(self):
        """Read in ship data

        Read in ship data from JSON file

        Parameters:
        ___________
          None

        Return:
        _______
          Boolean: True if successfully read, false otherwise
        """
        try:
            with open("data.json", "r") as dataFile: # open json file for reading
                jsonData = json.loads(dataFile.read()) # format json data
                # Parse json data into ships
                for ship in jsonData:
                    # Read each ship
                    boat = Ship(ship["name"], ship["size"], ship["symbol"])
                    if boat in self._ships:
                        print(f"ERROR: Ship {boat.getName()} already exists!")
                        return False
                    self._ships.append(boat) # Add to list of ships
                return True
        except IOError as error:
            # Catch file errors
            print(f"ERROR: {error}") # Print for debugging
            return False

    def isComputer(self):
        """Is the player a computer

        Returns False because board is meant for player.
        Purpose of function is to allow for polymorphism
        between player and computer.

        Parameters:
        ___________
          None

        Return:
        _______
          Boolean: True if a computer, false otherwise
        """
        return False

    def allSunk(self):
        """Check if all ships have been sunk

        Returns true if all ships are sunk

        Parameters:
        ___________
          None

        Return:
        _______
          Boolean: True if all ships sunk, false otherwise
        """
        for ship in self._ships:
            if not ship.isSunk():
                # If any ship is not sunk, then return false
                return False
        return True

    def hit(self, x, y):
        """Attack at coordinates

        Check if any ship exists at given coordinates

        Parameters:
        ___________
          x: X coordinate of attack
          y: Y coordinate of attack

        Return:
        _______
          Error: Enum for error states
          Flag: Enum for successful attacks
        """
        if x < 0 or x >= 10 or y < 0 or y >= 10:
            # Make sure that attack is within bounds
            return Error.OUT_OF_BOUNDS
        if self._board[y][x] == 'M' or self._board[y][x] == 'H' or self._board[y][x] == 'X':
            # Attack already made on the coordinates
            return Error.ALREADY_TRIED
        for ship in self._ships:
            # Check if coordinates collides with any ship 
            if ship.isHit(x, y):
                # Successful attack
                self._board[y][x] = 'H' # Set character on board
                if ship.isSunk():
                    # Ship is sunk
                    for pos in ship.getPos():
                        # Set to 'X' to indicate sunk
                        self._board[pos[1]][pos[0]] = 'X'
                    return Flag.SUNK # return that flag is sunk
                return Flag.HIT # Return successful hit
        self._board[y][x] = 'M' # Attack was a miss
        return Flag.MISS

    def clearPoint(self, x, y):
        """Clear all ships at the point

        Used to allow the user to remove a point 
        for the ship.

        Parameters:
        ___________
          x: X coordinate to remove
          y: Y coordinate to remove

        Return:
        _______
          None
        """
        if self._ships[self._currentShip].isSet(x, y):
            pos = self._ships[self._currentShip].getPos()
            if (x, y) == pos[0] or (x, y) == pos[-1]:
                self._board[y][x] = 'E' # Set to empty
                self._ships[self._currentShip].remove(x, y)

    def hasShip(self, x, y):
        """Check if a ship exists at the given coordinates

        Uses the board to check that the ship exists

        Parameters:
        ___________
          x: X coordinate to check
          y: Y coordinate to check

        Return:
        _______
          Boolean: True if a ship exists
        """
        return self._board[y][x] != 'E' and self._board[y][x] != 'H' and self._board[y][x] != 'M'

    def getCurrent(self):
        """Gets the current ship

        Used by the UI to iterate through and place each ship.

        Parameters:
        ___________
          None

        Return:
        _______
          Returns a ship
        """
        if self._currentShip >= 0 and self._currentShip < len(self._ships):
            # Make sure that current ship index is valid
            return self._ships[self._currentShip]
        else:
            return Error.OUT_OF_BOUNDS

    def next(self):
        """Move onto next ship

        Move to next ship

        Parameters:
        ___________
          None

        Return:
        _______
          None
        """
        if self._currentShip < len(self._ships):
            # Increment until end of list of ships
            self._currentShip += 1

    def allSet(self):
        """Check if all ships have been set

        Returns true if all ships have been set, False
        otherwise.

        Parameters:
        ___________
          None

        Return:
        _______
          Boolean: True if all ships are set
        """
        return self._currentShip == len(self._ships)

    def add(self, x, y):
        """Add a location for the current ship

        Add a ship onto the given coordinates.

        Parameters:
        ___________
          x: X coordinates
          y: Y coordinates

        Return:
        _______
          Error enum state
        """
        err = self._ships[self._currentShip].verifyLocation(x, y)
        if err == Error.ALREADY_SET:
            # Ship already set at coordinates
            return err
        elif self._board[y][x] != 'E':
            # Another ship exists at location
            return Error.SHIP_EXISTS
        if err == Error.NO_ERROR:
            # No error, add to board
            self._ships[self._currentShip].addLocation(x, y)
            self._board[y][x] = self._ships[self._currentShip].getSymbol()
            if self._ships[self._currentShip].allSet():
                self.next()
        return err

    def getChar(self, x, y):
        """Returns the character of the board

        Returns the character found at coordinate

        Parameter:
        __________
          x: X coordinate
          y: Y coordinate

        Return:
        _______
          Character at board
        """
        return self._board[y][x]

class ComputerBoard(PlayerBoard):
    """Represents the Computer player

    An object that represents the computer and 
    lets them randomly place ships, and make intelligent
    attacks.

    Attributes:
    ___________
      _hunt: Hunt mode to search for opponent ships
      _orientations: Orientation of ship to attack
      _moves: List of all moves made for intelligent attack
    """
    def __init__(self):
        """Creates a board for the computer

        Creates a player board for the computer/AI

        Parameters:
        ___________
          None

        Return:
        _______
          None
        """
        super().__init__()  # Call parent init
        self._hunt = True   # Hunt mode for computer attack
        self._orientations = [4, 3, 2, 1] # Orientations for attack
        self._moves = list() # All moves made for attack
        self._tries = 0

    def isComputer(self):
        """Checks if object is a computer

        Overloads function for type of object

        Parameters:
        ___________
          None

        Return:
        _______
          Boolean: True if object is a computer
        """
        return True

    def checkPos(self, x, y):
        """Finds orientation to place ship

        Makes sure that whole ship can be placed at
        the coordinates. Also determines which orientation
        for the ship is valid.

        Parameters:
        __________
          x: X coordinate
          y: Y coordinate

        Return:
        _______
          List of valid orientations for ship placement
        """
        choices = [1, 2, 3, 4] # Orientation for ship
        if self._board[y][x] != 'E':
            # x, y is not empty
            return []
        for i in range(0, self.getCurrent().getSize()):
            for j in range(0, self.getCurrent().getSize()):
                # Check in all directions
                if (x + i) >= 10:
                    if 1 in choices:
                        choices.remove(1) # Remove choice, if out of bounds
                else:
                    # Avoid clumping ships
                    if self._board[y][x+i] != 'E':
                        return []
                if (x - i) < 0:
                    if 2 in choices:
                        # out of bounds, remove choice
                        choices.remove(2)
                else:
                    # Avoid clumping ships
                    if self._board[y][x-1] != 'E':
                        return []
                if (y + j) >= 10:
                    # out of bounds remove choice
                    if 3 in choices:
                        choices.remove(3)
                else:
                    # Avoid clumping ships
                    if self._board[y+j][x] != 'E':
                        return []
                if (y - j) < 0:
                    # Out of bounds remove choice
                    if 4 in choices:
                        choices.remove(4)
                else:
                    # Avoid clumping ships
                    if self._board[y - j][x] != 'E':
                        return []
        return choices

    def placeShip(self):
        """Randomly place ships onto board

        Randomly places ships onto board for computer.
        Tries to avoid clumping in one area.

        Parameters:
        ___________
          None

        Return:
        _______
          None
        """
        while not self.allSet():
            # Place all ships
            choices = [] # orientations for ship
            while len(choices) == 0:
                # Get a random starting x, y coordinate for ship
                startX = random.randint(0, 9)
                startY = random.randint(0, 9)
                choices = self.checkPos(startX, startY) # get all valid orientations for ship
            orientation = random.choice(choices) # Set a random orientation
            size = self.getCurrent().getSize() # Get the size of the ship
            for i in range(0, size):
                # Place all of the ship
                self.add(startX, startY) # Start with the x, y and build from there
                if orientation == 1:
                    # 1 is in the positive x direction
                    startX += 1
                elif orientation == 2:
                    # 2 is the negative x direction
                    startX -= 1
                elif orientation == 3:
                    # 3 is the positive y direction
                    startY += 1
                elif orientation == 4:
                    # y is negative y direction
                    startY -= 1
        self._printBoard() # print board for debugging

    def _printBoard(self):
        """Print board to terminal

        Used for debugging purposes, prints location
        for all ships of computer.

        Parameters:
        ___________
          None

        Return:
        _______
          None
        """
        for i in range(0, 10):
            print(self._board[i]) # print board

    def makeMove(self):
        """Make an attack

        Generate an attack using an algorithm. Try
        to follow hits.

        Parameters:
        ___________
          None
        
        Return:
        ______
          None
        """
        if self._hunt:
            # Hunt mode - try random coordinates until hit is made
            while True:
                startX = random.randint(0, 9) # Random x coordinate 
                startY = random.randint(0, 9) # Random y coordinate
                if self._tries >= (10 * 10) / 2:
                    # already tried all parity based moves
                    break
                if (startX % 2 == 0 and startY % 2 == 0) or (startX % 2 == 1 and startY % 2 == 1):
                    # Make attack based on parity
                    break
            self._moves.clear() # clear all moves made
            self._moves.append((startX, startY)) # Start with the random coordinate
            return (startX, startY) # return the attempt
        else:
            # Target mode - hit has been made, find rest of ship
            while True:
                # Until another valid move is made
                x, y = self._moves[-1] # Build from the last move made
                nextMove = (0, 0) # Get the next move
                if self._orientations[-1] == 1:
                    # Check positive x direction for rest of ship
                    x += 1
                elif self._orientations[-1] == 2:
                    # Check negative x direction for rest of ship
                    y += 1
                elif self._orientations[-1] == 3:
                    # Check positive y direction for rest of ship
                    x -= 1
                elif self._orientations[-1] == 4:
                    # Check negative y direction for rest of ship
                    y -= 1
                nextMove = (x, y) # Try next move
                self._moves.append(nextMove) # Add to all moves
                if x >= 0 and x < 10 and y >= 0 and y < 10:
                    # Make sure move is within bounds
                    return nextMove
                else:
                    # Otherwise - check another orientation to test
                    self.adjustOrientation()

    def adjustOrientation(self):
        """Change orientation to target

        Changes orientation for intelligent attack.

        Parameters:
        ___________
          None

        Return:
        ______
          None
        """
        if not self._hunt:
            # If in target mode - remove last attack: unsuccessful
            self._moves.pop()
            self._orientations.pop()
        if len(self._orientations) == 0:
            # No more orientations 
            self._orientations = [4, 3, 2, 1] # Try again
            if len(self._moves) == 1:
                # No more moves, no longer target mode
                self._hunt = True
                self._moves.clear()
            else:
                del self._moves[1:] # start over from beginning

    def setHunt(self):
        """Set to hunt mode

        Set to hunt mode - randomly hunt

        Parameters:
        __________
          None

        Return:
        _______
          None
        """
        self._hunt = True # set to hunt mode
        self._orientations = [4, 3, 2, 1] # reset orientations

    def setTarget(self):
        """Set to target mode

        Target mode - intelligently find rest of ship

        Parameters:
        ___________
          None

        Return:
        ______
          None
        """
        self._hunt = False # set to target mode

    def countTries(self):
        """Counts how many tries have been made by computer

        This counts how many successful tries the computer made
        for attacks

        Parameters:
        ___________
          None

        Return:
        _______
          None
        """
        self._tries += 1
