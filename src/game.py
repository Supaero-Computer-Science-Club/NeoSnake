import curses
import time

from src.Snake import Snake

_wall = 10


def init_borders(y, x, h, w):
    top = [(y - 1, x + dx - 1) for dx in range(w + 2)]
    bottom = [(y + h, x + dx - 1) for dx in range(w + 2)]
    left = [(y + dy, x - 1) for dy in range(h)]
    right = [(y + dy, x + w) for dy in range(h)]
    return top, bottom, left, right


def blit(stdscr, borders, snake, apples, score, game_state, debug_msg, fps):
    stdscr.erase()

    for y, x in borders:
        stdscr.insch(y, x, ' ', curses.color_pair(_wall))

    snake.show(stdscr)
    for apple in apples:
        apple.show(stdscr)

    msgs = [
        # f"{snake.trail = }",
        # f"{len(snake.body) = }",
        f"{score = }",
        f"{game_state = }",
        f"{debug_msg = }"
    ]
    h = 0 if snake.get_head()[0] > curses.LINES // 2 else curses.LINES - len(msgs)
    for row, msg in zip(range(len(msgs)), list(map(str, msgs))):
        stdscr.addstr(h + row, 0, msg)

    stdscr.refresh()
    time.sleep(1 / fps)


def handle_input(c, game_state, scene, snake, apples):
    if c in [27, ord('q')]:
        return True, None, None

    reset = 0
    if c == ord('r'):
        if game_state != "play":
            snake.spawn(*scene)
            for apple in apples:
                apple.spawn(*scene)
            reset = 1
            game_state = "play"

    if c == 10:
        game_state = "menu" if game_state == "play" else "play"

    return False, 1 - reset, game_state


def menu():
    pass


def play(c, snake, apples, score):
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
            debug_msg = None
        return None, game_state, debug_msg
    else:
        return score + code, None, None
