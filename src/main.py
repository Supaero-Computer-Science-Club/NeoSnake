import curses

import sys

sys.path.append("./")
from src.Apple import Apple
from src.Snake import Snake
from src.errors import error_handler, CustomError

from src.game import _wall, init_borders, handle_input, play, menu, blit


@error_handler
def main(stdscr):
    # global game parameters.
    fps = 15
    scene = sx, sy, sh, sw = 1, 1, 34, 34
    nb_apples = 2
    init_length = 2
    swiftness = 1

    # check if everything can work properly.
    if (curses.LINES < sh + 2) or (curses.COLS < sw + 2):
        msg = f"terminal too small.\n" \
              f"expected at least {sw + 2, sh + 2} for a {sw, sh} game board, got {curses.COLS, curses.LINES}"
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
    game_state = "play"
    game_debug_msg = ''
    game_score = 0

    # the game loop.
    while True:
        c = stdscr.getch()

        # handle the game input.
        quit_game, reset, game_state = handle_input(c, game_state, scene, snake, apples)
        if quit_game:
            break
        game_score *= reset

        # run the current game state code snippet.
        if game_state == "menu":
            menu()
        elif game_state == "play":
            new_score, new_game_state, new_debug_msg = play(c, snake, apples, game_score)
            if new_score:
                game_score = new_score
            if new_game_state:
                game_state = new_game_state
            if new_debug_msg:
                game_debug_msg = new_debug_msg

        # blit all the objects on the screen.
        blit(stdscr, borders, snake, apples, game_score, game_state, game_debug_msg, fps)


if __name__ == "__main__":
    curses.wrapper(main)
