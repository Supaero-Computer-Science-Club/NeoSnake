import curses
import time

from Apple import Apple
from Snake import Snake


def main(stdscr):
    if not curses.can_change_color():
        raise Warning("Cannot change terminal colors...")
    curses.curs_set(0)
    stdscr.nodelay(1)

    scene = 0, 0, curses.LINES - 1, curses.COLS - 1
    snake = Snake(*scene)
    apple = Apple(*scene)

    fps = 15

    H = 20
    W = 20

    _wall = 10
    curses.init_color(_wall, 1000, 1000, 1000)
    curses.init_pair(_wall, _wall, _wall)

    play = True
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
            if not play:
                snake = Snake(*scene)
                apple = Apple(*scene)
                play = True

        if c == 10:
            curses.resizeterm(curses.LINES + 5, curses.COLS)

        snake.change_direction(c)
        if play:
            snake.move()
            if snake.update(snake.is_eating(apple)):
                play = False

        snake.show(stdscr)
        apple.show(stdscr)

        stdscr.refresh()
        time.sleep(1 / fps)


if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass
