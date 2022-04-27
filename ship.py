"""A Ship object

The Ship class represents a battle ship piece to be placed on the board
"""
from util import Error

class Ship:
    """Ship object

    An object that represents the battle ship piece.

    Attributes:
    ___________
      _name: name of the ship
      _size: size of the ship
      _symbol: symbol to represent ship
    """
    def __init__(self, name, size, symbol):
        """Constructor for creating a ship object

        Creates a ship object with a location, name, size,
        hit count, and whether it has been sunk
        
        Parameters:
        ___________
          name: Name of the ship
          size: Size of the ship

        Return:
        _______
          None
        """
        self._location = list() # List of all coordinates of ship location
        self._name = name  # Name of the ship
        self._size = size  # Size of the ship
        self._hitCount = 0 # How much of the ship has been hit
        self._sunk = False # Whether the ship has been sunk
        self._symbol = symbol 

    def isSunk(self):
        """Check if ship is sunk

        Return true if the ship is sunk, false otherwise
        
        Parameters:
        ___________
          None

        Return:
        _______
          Boolean
        """
        return self._sunk

    def isSet(self, x, y):
        """Check if location is already used

        Returns true if the ship has already been set
        at the given x, y coordinates.

        Parameters:
        ___________
          x: X coordinate to check
          y: Y coordinate to check

        Return:
        _______
          Boolean
        """
        return (x, y) in self._location # Check if coordinate in location list

    def allSet(self):
        """Check if ship is all set

        Returns True if all points for the ship has been set

        Parameters:
        ___________
          None

        Return:
        _______
          Boolean
        """
        return len(self._location) == self._size # Check if there are coordinates for the whole size of ship

    def getName(self):
        """Returns the name of the ship

        Returns the name of the ship

        Parameters:
        ___________
          None

        Return:
        _______
          Name of the ship
        """
        return self._name # Return name of ship

    def getSymbol(self):
        """Returns the name of the ship

        Returns the name of the ship

        Parameters:
        ___________
          None

        Return:
        _______
          Name of the ship
        """
        return self._symbol # Return name of ship


    def getSize(self):
        """Returns the size of the ship

        Returns the size of the ship

        Parameters:
        ___________
          None

        Return:
        _______
          Size of ship
        """
        return self._size # Return size of the ship

    def getPos(self):
        """Get a list of the location of the ship

        Returns a list of all the coordinates of the ship,
        represented as a tuple

        Parameters:
        ___________
          None

        Return:
        _______
          List of tuple coordinates
        """
        return self._location # list of tuple coordinates

    def addLocation(self, x, y):
        """Add coordinate to list of ships

        Adds tuple of coordinate to location of ship

        Parameters:
        ___________
          x: X coordinate for ship
          y: Y coordinate for ship

        Return:
        _______
          None
        """
        self._location.append((x, y)) # Add coordinates to list

    def remove(self, x, y):
        """Remove coordinate for ship

        Removes the coordinate tuple for the ship

        Parameters:
        ___________
          x: X coordinate to remove
          y: Y coordinate to remove

        Return:
        _______
          None
        """
        if (x, y) in self._location:
            # check that x, y is in the list
            self._location.remove((x, y)) # remove if in list

    def hitShip(self):
        """Increase hit count of the ship

        Ship has been hit, increase hit count

        Parameters:
        ___________
          None

        Return:
        _______
          Boolean: True if ship is sunk
        """
        if not self._sunk:
            # if ship is not already sunk
            self._hitCount += 1 # increment hit counter
            if self._hitCount == self._size:
                # if ship is sunk
                self._sunk = True # sunk is true

    def isHit(self, x, y):
        """Make an attack at given coordinates

        Check if x, y coordinates are a hit.

        Parameters:
        ___________
          x: X coordinate to attack
          y: Y coordinate to attack

        Return:
        _______
          Boolean - True if successful attack
        """
        if (x, y) in self._location and not self._sunk:
            # Make sure that there is a ship at the coordinate
            # And the ship is not already sunk
            self.hitShip() # Hit the ship
            return True # True if the ship has been hit
        else:
            return False # False otherwise

    def verifyLocation(self, x, y):
        """Verify the location for the ship

        Used when placing coordinates for the ship to
        verify that the given coordinates are valid.
        We assume that the x, y is a valid index, as checked
        by the UI.

        Parameters:
        ___________
          x: X coordinate to check
          y: Y coordinate to check

        Return:
        _______
          Error enum is returned based on error state
        """
        if len(self._location) == 0:
            # The first location is always valid
            return Error.NO_ERROR
        elif self.isSet(x, y):
            # The coordinate has already been set
            return Error.ALREADY_SET
        else:
            for coordinate in self._location:
                # Check that coordinate is not along diagonal
                posX = abs(coordinate[0] - x) # get distance in x direction
                posY = abs(coordinate[1] - y) # get distance in y direction
                if posX == 1 and posY == 1:
                    return Error.DIAGONAL
            for coordinate in self._location:
                # Check that coordinate is adjacent to another point
                posX = abs(coordinate[0] - x)
                posY = abs(coordinate[1] - y)
                if (posX == 1 and posY == 0) or (posY == 1 and posX == 0):
                    # No error if it is adjacent not along diagonal
                    return Error.NO_ERROR
            return Error.SPREAD_APART # Coordinates not adjacent

    def __eq__(self, other):
        """Checks if two ships are equal to each other

        A ship is considered equal if they have the same name

        Parameters:
        ___________
          other: ship object to compare

        Return:
        _______
          Boolean: True if the two ships are the same, false otherwise
        """
        return self._name == other.getName()
