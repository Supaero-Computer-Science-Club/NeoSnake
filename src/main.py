import curses

import os
import sys

# allows the user to play from anywhere in the system.
path = os.path.dirname(os.path.realpath(__file__)) + "/.."
sys.path.append(path)
from src.Apple import Apple
from src.Snake import Snake

from src.errors import CustomError
from src.errors import curses_wrapper
from src.errors import error_handler_wrapper

from src.game import _wall
from src.game import PLAY
from src.game import MENU
from src.game import init_borders
from src.game import handle_input
from src.game import menu
from src.game import play
from src.game import blit


@error_handler_wrapper
@curses_wrapper
def main(stdscr):
    # global game parameters.
    fps = 15
    scene = sx, sy, sh, sw = 1, 1, 34, 34
    nb_apples = 2
    init_length = 2
    swiftness = 1

    # check if everything can work properly.
    if (curses.LINES < sh + 2) or (curses.COLS < sw + 2):
        d_lines, d_cols = max(0, sh + 2 - curses.LINES), max(0, sw + 2 - curses.COLS)
        msg = f"terminal too small.\n" \
              f"expected at least {sw + 2, sh + 2} for a {sw, sh} game board, got {curses.COLS, curses.LINES}\n" \
              f"please increase terminal's width by {d_cols} pixel{'s' if d_cols > 1 else ''} and " \
              f"its height by {d_lines} pixel{'s' if d_lines > 1 else ''}"
        raise CustomError(msg)

    if curses.can_change_color():
        curses.init_color(_wall, 1000, 1000, 1000)
        curses.init_pair(_wall, _wall, _wall)
    else:
        curses.init_pair(_wall, curses.COLOR_WHITE, curses.COLOR_WHITE)

    curses.curs_set(0)
    stdscr.nodelay(1)

    # all the objects in the scene.
    top_border, bottom_border, left_border, right_border = init_borders(*scene)
    borders = top_border + bottom_border + left_border + right_border
    snake = Snake(swiftness=swiftness)
    apples = [Apple() for _ in range(nb_apples)]

    # spawn the spawnable objects.
    snake.spawn(*scene, init_length=init_length)
    for apple in apples:
        apple.spawn(*scene)

    # internal variables of the game.
    game_state = PLAY
    game_debug = False
    game_debug_msg = ''
    game_score = 0

    # the game loop.
    while True:
        c = stdscr.getch()

        # handle the game input.
        quit_game, reset, game_state, switch_debug = handle_input(c, game_state, scene, snake, apples)
        if quit_game:
            break
        game_debug ^= switch_debug
        game_score *= reset

        # run the current game state code snippet.
        if game_state == MENU:
            menu()
        elif game_state == PLAY:
            new_score, new_game_state, new_debug_msg = play(c, snake, apples, game_score)
            game_score = new_score if new_score else game_score
            game_state = new_game_state if new_game_state else game_state
            game_debug_msg = new_debug_msg if new_debug_msg else game_debug_msg

        # blit all the objects on the screen.
        blit(stdscr, borders, snake, apples, game_score, game_state, game_debug, game_debug_msg, fps)


if __name__ == "__main__":
    main()
