import curses
import time

from Apple import Apple
from Snake import Snake


def main(stdscr):
    if not curses.can_change_color():
        raise Warning("Cannot change terminal colors...")
    curses.curs_set(0)
    stdscr.nodelay(1)

    snake = Snake()
    apple = Apple()

    fps = 15

    play = True
    while True:
        stdscr.erase()

        snake.change_direction(stdscr.getch())
        if play:
            snake.move()
            if snake.update(snake.is_eating(apple)):
                play = False

        snake.show(stdscr)
        apple.show(stdscr)

        stdscr.refresh()
        time.sleep(1 / fps)


if __name__ == "__main__":
    curses.wrapper(main)
