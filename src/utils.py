import curses
import os

import numpy as np

from curses.textpad import rectangle
from curses.textpad import Textbox

# directories initializations.
_root = os.path.dirname(os.path.realpath(__file__)) + "/.."
_log = os.path.join(_root, ".log")
if not os.path.exists(_log):
    os.makedirs(_log)
_log = os.path.join(_log, "log")


def log(*args, sep=' ', end='\n'):
    """
        Logs a list of elements inside the './.log/log' file.

        Args
        ----
        args : list of anything with a str method
            all the elements to log into 'log.log'
        sep : str
            the separator between each element.
        end : str
            the end of the final string that will be logged.

        Returns
        -------
        None
    """
    with open(_log, 'a') as file:
        file.write(sep.join(map(str, args)) + end)


def init_color_palette(r_bits=3, g_bits=3, b_bits=2):
    """
        Initializes the color palette for the terminal.
        Colors are coded with 8 bits, namely, the sum of r_bits, g_bits and b_bits should remain equal to 8.

        Args
        ----
        r_bits : 0 <= int <= 8
            the number of bits allocated to the red channel.
        g_bits : 0 <= int <= 8
            the number of bits allocated to the green channel.
        b_bits : 0 <= int <= 8
            the number of bits allocated to the blue channel.

        Returns
        -------
        None
    """
    s_bits = r_bits + g_bits + b_bits
    if s_bits != 8:
        raise Warning(f"colors are coded with 8 bits: got r:{r_bits} + g:{g_bits} + b:{b_bits} = {s_bits} instead.")

    # all the possible values for the channels.
    reds = np.linspace(0, 1000, 2 ** r_bits).astype(int)
    greens = np.linspace(0, 1000, 2 ** g_bits).astype(int)
    blues = np.linspace(0, 1000, 2 ** b_bits).astype(int)

    # the masks to isolate the colors parts.
    r_mask, g_mask, b_mask = (2 ** r_bits - 1), (2 ** g_bits - 1), (2 ** b_bits - 1)

    # the color loop.
    for color in range(1, 256):
        # isolate the channels.
        r, g, b = (color >> (b_bits + g_bits)) & r_mask, (color >> b_bits) & g_mask, (color >> 0) & b_mask
        # store the colors in memory.
        curses.init_color(color, reds[r], greens[g], blues[b])
        curses.init_pair(color, curses.COLOR_BLACK, color)


# def paint(stdscr, y, x, _r, _g, _b, bits=3):
#     color = (_r << (2 * bits)) + (_g << bits) + _b
#     stdscr.addstr(y, x, ' ', curses.color_pair(8 + color))


def prompt_user(stdscr, msg='', box=(1, 15, 1, 0)):
    """
        Prompts the user by creating an editable box and returning the resulting input string of characters.

        Args
        ----
        stdscr : _curses.window
            the screen object.
        msg : str, optional
            a message explaining the prompt.
        box : (int, int, int, int), optional
            the rectangle representing the geometry of the prompt box. Namely, (h, w, y, x) with y and x starting at 0.

        Returns
        -------
        input : str
            a string given by the user as an input.
    """
    # print the message above the box.
    stdscr.addstr(box[2] - 1, 0, msg)

    h, w, y, x = box
    editwin = curses.newwin(h, w, y + 1, x + 1)  # curses.newwin starts positions at 1.
    rectangle(stdscr, y, x, box[2] + box[0] + 1, box[3] + box[1] + 1)
    stdscr.refresh()

    # create the box and edit it.
    box = Textbox(editwin)
    box.edit()

    # return the content of the box as the result.
    return box.gather()
