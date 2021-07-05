import numpy as np

from src.utils import log


class Apple:
    """
        The apple in the Snake game.
    """

    def __init__(self, asset='o'):
        """
            Creates a new empty apple.

            Args
            ----
            asset : character
                the character used to display the apple.
        """
        self.pos = None
        self.asset = asset

    def spawn(self, y, x, h, w):
        """
            Spawns the apple inside the game area.

            Args
            ----
            y : int
                the y coordinate of the top left corner of the game area.
            x : int
                the x coordinate of the top left corner of the game area.
            h : int
                the height of the game area.
            w : int
                the width of the game area.
        """
        self.pos = (np.random.randint(y, y + h), np.random.randint(x, x + w))
        log(self.pos)

    def show(self, stdscr):
        """
            Displays the apple on the screen.

            Args
            ----
            stdscr : _curses.window
                the window on which to display the object.

            Returns
            -------
            None
        """
        stdscr.addstr(*self.pos, self.asset)
