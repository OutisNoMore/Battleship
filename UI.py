"""An User Interface created with pygame to play Battleship

The GameBase class creates an interface for the user to play battleship
The game itself is run by classes from the util module. The Window enum
represents the different windows used in the game.

References
__________
  https://stackoverflow.com/questions/36932/how-can-i-represent-an-enum-in-python
  https://stackoverflow.com/questions/33963361/how-to-make-a-grid-in-pygame
  https://www.pygame.org/docs/ref/font.html
"""
from enum import Enum
from util import Window, Error, Flag
from player import PlayerBoard, ComputerBoard
import pygame

class Text(pygame.sprite.Sprite):
    def __init__(self, x, y, text):
        super().__init__()
        self.image = text
        self.rect =self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Cell(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("bluetile.jpg").convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class GameBase:
    """Base class for printing the game

    Handles the front end: displays game board, and moves
    for both the user and the computer players.

    Attributes:
    ___________
      _width: width of the board
      _height: height of the board
      _display: display screen
      _gameOver: Keep track of if game is over
      _win: Whether the player won
      _window: window to display
      _player: Player object to make moves
      _computer: Computer player object to make moves
      _title: font to print title
      _text: font to print text
    """
    def __init__(self, width, height):
        """Constructor that creates the game screen with the given dimensions

        Create a screen with set width and height to play the game, and all
        windows.

        Parameters:
        ___________
        width: Width of the screen
        height: Height of the screen

        Return:
        _______
        None
        """
        pygame.init()
        self._width = width   # width of screen
        self._height = height # height of screen
        self._display = pygame.display.set_mode((self._width, self._height)) # display screen
        self._gameOver = False # Keep track of if game is over
        self._win = False      # Did the player win, False = Computer won
        self._window = Window.PLACE_SHIP # keep track of window to display
        self._player = PlayerBoard() # Player Board
        self._computer = ComputerBoard() # Create Computer
        self._title = pygame.font.SysFont("Arial", 50) # Title Font
        self._text = pygame.font.SysFont("Arial", 25)  # Text Font
        self._boardX = 0 # X coordinate of board
        self._sprites = pygame.sprite.LayeredUpdates()
        self.drawGrid((self._width // 2) -250, 200, self._player) # draw player board
        text = self._title.render("Battleship", False, (0, 0, 0)) # generate title text
        x = (self._width // 2) - (text.get_rect().width // 2) # center text
        title = Text(x, 10, text)
        self._sprites.add(title)

    def mouseButtonDown(self, x, y):
        """Handles mouse click events

        Processes mouse click events, given the x, y coordinates of 
        the where the mouse was clicked. Depending on what window
        the game is on, events are handled differently.

        Parameters:
        ___________
          x: X coordinate on screen where mouse was clicked
          y: Y coordinate on screen where mouse was clicked
        
        Returns:
        ________
          Nothing is returned
        """
        if self._gameOver:
            # Do not handle events if game is over
            return
        if self._window == Window.PLACE_SHIP:
            # Handle mouse click events when user is placing ships
            if (x >= 500 and x < 1000) and (y >= 200 and y < 700):
                # Make sure that x,y is inside player's grid
                posX = (x - 500) // 50 # convert to array index
                posY = (y - 200) // 50 # convert to array index
                err = self._player.add(posX, posY) # add ship coordinate to player board
                text = self._text.render(f"{self._player.getChar(posX, posY)}", False, (0, 0, 0))
                x = 500 + (posX * 50) 
                y = 200 + (posY * 50)
                if err == Error.ALREADY_SET:
                    # Allow user to delete a point for current ship
                    self._player.clearPoint(posX, posY)
                    self._sprites.get_sprites_at((x, y))[1].kill()
                elif err == Error.NO_ERROR:
                    self._sprites.add(Text(x, y, text))
        elif self._window == Window.PLAYER_TURN:
            # Handle mouse click events when the player is attacking
            if (x >= self._boardX + 600 and x < self._boardX + 1100) and (y >= 200 and y < 700):
                # Make sure that x, y is inside the computer's grid
                posX = (x - self._boardX - 600) // 50 # convert to array index
                posY = (y - 200) // 50 # convert to array index
                result = self._computer.hit(posX, posY) # try attack on computer grid
                if result == Flag.MISS:
                    color = (255, 0, 0)
                    text = self._text.render(f"{self._computer.getChar(posX, posY)}", False, color)
                    self._sprites.add(Text(self._boardX + 600 + posX*50, 200 + posY*50, text))
                    self._window = Window.COMPUTER_TURN
                if result == Flag.SUNK or result == Flag.HIT:
                    # make sure that result is valid
                    color = (0, 200, 0)
                    text = self._text.render(f"{self._computer.getChar(posX, posY)}", False, color)
                    self._sprites.add(Text(self._boardX + 600 + posX*50, 200 + posY*50, text))
                    if self._computer.allSunk():
                        # If all ships have been sunk
                        self._window = Window.GAME_OVER # Change to Game over window
                        self._win = True # User has won
                    else:
                        # Otherwise, it is the computer's turn
                        self._window = Window.COMPUTER_TURN

    def drawGrid(self, posX, posY, player):
        """Draw a grid onto the screen

        Draws a 2D grid onto the screen. Include all
        ship, hits, and miss data as well.

        Parameters:
        ___________
          posX: X coordinate on screen to print grid
          posY: Y coordinate on screen to print grid
          player: PlayerBoard object to print grid from
        
        Returns:
        ________
          Nothing is returned - Grid is printed on screen
        """
        blockSize = 45 # Set the size of the grid block
        for x in range(posX, posX + 10*(blockSize+5), blockSize + 5):
            for y in range(posY, posY + 10*(blockSize+5), blockSize + 5):
                self._sprites.add(Cell(x, y))
                #rect = pygame.Rect(x, y, blockSize, blockSize) # draw grid using squares
                #pygame.draw.rect(self._display, (0, 0, 0), rect, 1) # draw onto screen
                offsetX = (x - posX) // 50 # calculate array index
                offsetY = (y - posY) // 50 # calculate array index
                char = player.getChar(offsetX, offsetY) # get character at location
                color = (0, 0, 0) # color code to print each character
                if char == 'E':
                    # Grid is empty at the coordinate
                    continue 
                if not player.isComputer():
                    # Print user computer
                    if char == 'H': color = (255, 0, 0)   # Hits taken are red
                    elif char == 'M': color = (0, 255, 0) # Misses are green
                    else: color = (0, 0, 255)             # Ships are printed in blue
                elif player.isComputer(): 
                    # Print computer board
                    if char == 'H': color = (0, 255, 0)   # Successful hits are green
                    elif char == 'M': color = (255, 0, 0) # Misses made are red
                    elif char == 'X': color = (0, 0, 255) # X to indicate sunken ship
                    else: continue # don't print ships
                self.boardText(color, char, (x, y)) # draw characters onto grid

    def boardText(self, color, char, point):
        """Draw text onto the grid

        Draws a character representing whether the
        grid at the coordinate is a hit, miss, or a
        ship.

        Parameters:
        ___________
          color: 3-tuple for color of character
          char: Character to print
          point: x, y tuple for location of char

        Return:
        _______
          None
        """
        text = self._text.render(char, False, color) # Create text to print
        self._sprites.add(Text(point[0], point[1], text))
        #self._display.blit(text, point) # Draw onto screen

    def placeShip(self):
        """Window for player to place ships on their board

        Displays the player's grid, and allows user to
        choose coordinates for each ship

        Parameters:
        ___________
          None

        Return:
        _______
          None
        """
        if self._player.allSet():
            # If all ships have been set, move to next window
            self._window = Window.PLAYER_TURN # Now player's turn to playgame
            self._sprites.empty()
            title = self._title.render("Battleship", False, (0, 0, 0)) # Game over text
            x = (self._width // 2) - (title.get_rect().width // 2)   # get x coordinate for center of screen
            self._sprites.add(Text(x, 10, title))
            self._boardX = (self._width // 2) - (1100 // 2) # center boards
            self.drawGrid(self._boardX, 200, self._player)   # print final player board
            self.drawGrid(self._boardX + 600, 200, self._computer) # print final computer board
        else:
            # Allow user to place ships
            text = self._text.render(f"Place: {self._player.getCurrent().getName()}", False, (0, 0, 0)) # text to indicate which ship to place
            x = (self._width // 2) - 250 # x coordinate for text
            self._display.blit(text, (x, 200 - text.get_rect().height - 5)) # Put text on screen

    def computerTurn(self):
        """Window to displaywhen it is the computer's turn

        The computer makes its move at this point. This window
        passes very quickly, and so is usually just an attack
        that appears on the player's grid.

        Parameters:
        ___________
          None

        Return:
        _______
          None
        """
        coordinate = self._computer.makeMove()  # Get coordinates for computer's move
        err = self._player.hit(coordinate[0], coordinate[1]) # Make attack onto player's board
        if err == Error.ALREADY_TRIED:
            # Coordinate has already been tried, try again
            self._computer.adjustOrientation() # Change direction to try
            return
        elif self._player.allSunk():
            # All ships have been sunk, computer wins
            self._window = Window.GAME_OVER # go to game over
            color = (255, 0, 0)
        elif err == Flag.HIT:
            # Successful attack
            self._computer.setTarget() # Set computer to target mode
            self._window = Window.PLAYER_TURN # Is now player's turn
            color = (255, 0, 0)
        elif err == Flag.SUNK:
            # Ship has been sunk
            self._computer.setHunt() # Set computer to hunt mode
            self._window = Window.PLAYER_TURN # Is now player's turn
            color = (255, 0, 0)
        elif err == Flag.MISS:
            # Attack unsuccessful, miss
            self._computer.adjustOrientation() # Change direction of attack
            self._window = Window.PLAYER_TURN  # Now player's turn
            color = (0, 200, 0)
        text = self._text.render(f"{self._player.getChar(coordinate[0], coordinate[1])} ", False, color, (5, 225, 250))
        ch = Text(self._boardX + (coordinate[0] * 50), 200 + (coordinate[1]*50), text)
        self._sprites.add(ch)

    def gameOver(self):
        """Game over window

        Draws the final board, and prints game over, and
        the winner.

        Parameters:
        ___________
          None

        Return:
        _______
          None
        """
        title = self._title.render("Game Over", False, (255, 0, 0), (200, 200, 200))
        x = (self._width // 2) - (title.get_rect().width // 2)
        y = (self._height // 2) - (title.get_rect().height // 2)
        self._display.blit(title, (x, y)) # draw winner onto screen
        if self._win:
            # Player wins
            output = "You Win!"
        else:
            # Computer wins
            output = "You Lose!"
        text = self._text.render(output, False, (0, 0, 0), (200, 200, 200)) # Text for who is winner
        x = (self._width // 2) - (text.get_rect().width // 2) # x coordinate for center of screen
        y = y + title.get_rect().height + 10 # y coordinate 10 pixels under game over text
        self._display.blit(text, (x, y)) # draw winner onto screen

    def update(self):
        """Updates screen based on window
        
        Makes sure that correct window is called for the update.

        Parameters:
        ___________
          None

        Return:
        _______
          None
        """
        if self._window != Window.PLACE_SHIP:
            text = self._text.render("Player Board", False, (0, 0, 0)) # Label player board
            newX = (250 - text.get_rect().width // 2) # center text on board
            newY = 200 - (text.get_rect().height + 10)
            self._display.blit(text, (self._boardX + newX, newY)) # draw Text
            text = self._text.render("Computer Board", False, (0, 0, 0)) # Label computer board
            newX = (250 - text.get_rect().width // 2) # center text on board
            newY = 200 - (text.get_rect().height + 10)
            self._display.blit(text, (self._boardX + newX + 600, newY)) # draw text
        if self._window == Window.PLACE_SHIP:
            # Go to place ship window
            self.placeShip()
        elif self._window == Window.COMPUTER_TURN:
            # Go to window for the computer's turn
            self.computerTurn()
        elif self._window == Window.GAME_OVER:
            # Go to game over window
            self.gameOver()

    def run(self):
        """Starts running the game

        Uses update function to show windows.
        Handles user events through clicks.

        Parameters:
        ___________
          None

        Return:
        _______
          None
        """
        while not self._gameOver:
            # play game
            for event in pygame.event.get():
                # handle user events
                if event.type == pygame.QUIT:
                    # if exit button pressed - quit game
                    self._gameOver = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # handle all mouse clicks
                    self.mouseButtonDown(event.pos[0], event.pos[1])
            self._display.fill((255, 255, 255)) # fill background with white
            self._sprites.draw(self._display)
            self.update() # update variables/sprite 
            pygame.display.update() # update display
        pygame.quit() # Quit pygame

if __name__ == "__main__":
    WIDTH = 1500 # 1500 px width of screen
    HEIGHT = 800 # 800 px height of screen
    game = GameBase(WIDTH, HEIGHT) # create game object
    game.run() # run the game
