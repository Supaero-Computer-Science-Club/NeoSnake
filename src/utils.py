import curses

import numpy as np


def log(*args, sep=' ', end='\n'):
    """
        Logs a list of elements inside the 'log.log' file.

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
    with open("log.log", 'a') as file:
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
