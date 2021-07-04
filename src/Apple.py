import numpy as np


class Apple:
    def __init__(self, y, x, h, w):
        self.pos = None
        self.spawn(y, x, h, w)

    def spawn(self, y, x, h, w):
        self.pos = (np.random.randint(y+1, y + h - 1), np.random.randint(x+1, x + w - 1))

    def show(self, stdscr):
        stdscr.addstr(*self.pos, 'O')
