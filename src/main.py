import curses

import os
import sys

# allows the user to play from anywhere in the system.
from datetime import datetime

_root = os.path.dirname(os.path.realpath(__file__)) + "/.."
sys.path.append(_root)

from src.Apple import Apple
from src.Snake import Snake

from src.errors import CustomError
from src.errors import curses_wrapper
from src.errors import error_handler_wrapper

import src.game as game


@error_handler_wrapper
@curses_wrapper
def main(stdscr):
    # global game parameters.
    fps = 15
    scene = sx, sy, sh, sw = 1, 1, 34, 34
    nb_apples = 2
    init_length = 2
    swiftness = 1
    user_name = game.get_user_name(stdscr)

    # check if everything can work properly.
    if (curses.LINES < sh + 2) or (curses.COLS < sw + 2):
        d_lines, d_cols = max(0, sh + 2 - curses.LINES), max(0, sw + 2 - curses.COLS)
        msg = f"terminal too small.\n" \
              f"expected at least {sw + 2, sh + 2} for a {sw, sh} game board, got {curses.COLS, curses.LINES}\n" \
              f"please increase terminal's width by {d_cols} pixel{'s' if d_cols > 1 else ''} and " \
              f"its height by {d_lines} pixel{'s' if d_lines > 1 else ''}"
        raise CustomError(msg)

    if curses.can_change_color():
        curses.init_color(game.WALL, 1000, 1000, 1000)
        curses.init_pair(game.WALL, game.WALL, game.WALL)
    else:
        curses.init_pair(game.WALL, curses.COLOR_WHITE, curses.COLOR_WHITE)

    curses.curs_set(0)
    stdscr.nodelay(1)

    # all the objects in the scene.
    top_border, bottom_border, left_border, right_border = game.init_borders(*scene)
    borders = top_border + bottom_border + left_border + right_border
    snake = Snake(swiftness=swiftness)
    apples = [Apple() for _ in range(nb_apples)]

    # spawn the spawnable objects.
    snake.spawn(*scene, init_length=init_length)
    for apple in apples:
        apple.spawn(*scene)

    # internal variables of the game.
    game_state = game.PLAY
    game_debug = False
    game_debug_msg = ''
    game_score = 0
    game_scores = []

    # the game loop.
    while True:
        c = stdscr.getch()

        # handle the game input.
        quit_game, reset, game_state, switch_debug = game.handle_input(c, game_state, scene, snake, apples)
        if quit_game:
            with open(".scores.csv", "w") as file:
                content = '\n'.join(map(str, game_scores))
                file.write(content)
            break
        game_debug ^= switch_debug
        game_score *= reset

        # run the current game state code snippet.
        if game_state == game.MENU:
            game.menu()
        elif game_state == game.PLAY:
            new_score, new_game_state, new_debug_msg = game.play(c, snake, apples, game_score)
            game_score = new_score if new_score else game_score
            game_state = new_game_state if new_game_state else game_state
            game_debug_msg = new_debug_msg if new_debug_msg else game_debug_msg
        elif game_state == game.LOST:
            game_state = game.WAITING
            data = [game_score, datetime.now().strftime("%d/%m/%Y %H:%M:%S"), user_name]
            game_scores.append(';'.join(map(str, data)))

        # blit all the objects on the screen.
        game.blit(stdscr, borders, snake, apples, game_score, game_state, game_debug, user_name + game_debug_msg, fps)


if __name__ == "__main__":
    main()
