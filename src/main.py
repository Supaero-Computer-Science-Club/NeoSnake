import curses
import time

import sys

sys.path.append("./")
from src.Apple import Apple
from src.Snake import Snake
from src.utils import log


def main(stdscr):
    fps = 15
    scene = 0, 0, 30, 30
    nb_apples = 10
    init_length = 10

    log(type(stdscr))
    if curses.can_change_color():
        _wall = 10
        curses.init_color(_wall, 1000, 1000, 1000)
        curses.init_pair(_wall, _wall, _wall)
    else:
        _wall = 1
        curses.init_pair(_wall, curses.COLOR_WHITE, curses.COLOR_WHITE)

    curses.curs_set(0)
    stdscr.nodelay(1)

    snake = Snake()
    apples = [Apple() for _ in range(nb_apples)]
    snake.spawn(*scene, init_length=init_length)
    for apple in apples:
        apple.spawn(*scene)

    game_state = "play"
    debug_msg = ''
    score = 0
    while True:
        stdscr.erase()

        for y, x in [(scene[0], scene[1] + x) for x in range(scene[3])] + \
                    [(scene[0] + scene[2] - 1, scene[1] + x) for x in range(scene[3])] + \
                    [(scene[0] + y, scene[1]) for y in range(1, scene[2])] + \
                    [(scene[0] + y, scene[1] + scene[3] - 1) for y in range(1, scene[2])]:
            stdscr.addch(y, x, ' ', curses.color_pair(_wall))

        if curses.is_term_resized(curses.LINES, curses.COLS):
            pass

        c = stdscr.getch()

        if c in [27, ord('q')]:
            break

        if c == ord('r'):
            if game_state != "play":
                snake.spawn(*scene)
                for apple in apples:
                    apple.spawn(*scene)
                score = 0
                game_state = "play"

        if c == 10:
            game_state = "menu" if game_state == "play" else "play"

        if game_state == "play":
            snake.change_direction(c)
            snake.move()
            code = snake.update(snake.is_eating(apples))
            if code < Snake.NOTHING:
                curses.beep()
                game_state = "lost"
                if code == Snake.OUTSIDE:
                    debug_msg = f"hit walls -> {score}"
                elif code == Snake.SELF_BITE:
                    debug_msg = f"self_intersect -> {score}"
            else:
                score += code

        snake.show(stdscr)
        for apple in apples:
            apple.show(stdscr)

        msgs = [
            f"{snake.trail = }",
            f"{len(snake.body) = }",
            f"{score = }",
            f"{game_state = }",
            f"{debug_msg = }"
        ]
        h = 0 if snake.get_head()[0] > curses.LINES // 2 else curses.LINES - 1 - len(msgs)
        for row, msg in zip(range(len(msgs)), list(map(str, msgs))):
            stdscr.addstr(h + row, 0, msg)

        stdscr.refresh()
        time.sleep(1 / fps)


if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass
