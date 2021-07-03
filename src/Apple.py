import curses

import numpy as np


class Apple:
    def __init__(self):
        self.pos = (np.random.randint(curses.LINES), np.random.randint(curses.COLS))

    def spawn(self):
        self.pos = (np.random.randint(curses.LINES), np.random.randint(curses.COLS))

    def show(self, stdscr):
        stdscr.addstr(*self.pos, 'O')
