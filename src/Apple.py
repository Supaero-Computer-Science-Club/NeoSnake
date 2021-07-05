import numpy as np


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
            y : 0 <= int < curses.LINES
                the y coordinate of the top left corner of the game area.
            x : 0 <= int < curses.COLS
                the x coordinate of the top left corner of the game area.
            h : 0 <= int < curses.LINES - y
                the height of the game area.
            w : 0 <= int < curses.COLS - x
                the width of the game area.

            Returns
            -------
            None
        """
        self.pos = (np.random.randint(y, y + h), np.random.randint(x, x + w))

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
