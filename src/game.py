import curses
import os
import time

from src.Snake import Snake
from src.utils import prompt_user

WALL = 10

MENU = 1
PLAY = 2
LOST = 3
WAITING = 4


def init_borders(y, x, h, w):
    """
        Initializes the borders of the game board.

        Args
        ----
        y : 0 <= int < curses.LINES
            the y coordinate of the top left corner of the game area.
        x : 0 <= int < curses.COLS
            the x coordinate of the top left corner of the game area.
        h : 0 <= int < curses.LINES - y
            the height of the game area.
        w : 0 <= int < curses.COLS - x
            the width of the game area.

        Returns
        -------
        top, bottom, left, right : tuple of list of int 2-uples
            the positions of all the cells constituting the borders of the board.
    """
    top = [(y - 1, x + dx - 1) for dx in range(w + 2)]
    bottom = [(y + h, x + dx - 1) for dx in range(w + 2)]
    left = [(y + dy, x - 1) for dy in range(h)]
    right = [(y + dy, x + w) for dy in range(h)]
    return top, bottom, left, right


def handle_input(c, game_state, scene, snake, apples):
    """
        Handles the input of the game.

        Args
        ----
        c : int
            the input code.
        game_state : int
            the current state of the game.
        scene : 4-uple of ints
            the geometry of the game area.
        snake : src.Snake.Snake
            the snake.
        apples : list of src.Apple.Apple instances.
            all the apples in the game.

        Returns
        -------
        quit, reset, new_game_state, swicth_debug : bool, int, int, bool
            a signal telling if the game is over, a reset integer for the score, the new state of the game and a debug
            switching signal.
    """
    # quit the game.
    if c in [27, ord('q')]:
        return True, None, None, False

    # respawn the objects if 'r' is pressed whilst not playing
    reset, new_game_state, switch_debug = 0, game_state, False
    if c == ord('r'):
        if game_state in [LOST, WAITING]:
            snake.spawn(*scene)
            for apple in apples:
                apple.spawn(*scene)
            reset = 1
            new_game_state = PLAY

    # switch between the menu and the play when 'enter' is pressed.
    if c == 10:
        new_game_state = MENU if game_state == PLAY else PLAY

    # switches the debug pannel.
    if c == ord('d'):
        switch_debug = True

    return False, 1 - reset, new_game_state, switch_debug


def menu():
    """
        ---

        Args
        ----

        Returns
        -------
    """
    pass


def play(c, snake, apples, score):
    """
        Plays one step of the game of Snake.

        Args
        ----
        c : int
            the input code.
        snake : src.Snake.Snake
            the snake.
        apples : list of src.Apple.Apple instances.
            all the apples in the game.
        score : int
            the current score in the game.

        Returns
        -------
        new_score, new_game_state, new_debug_msg : int, int, str
            the new score, the new state of the game, the new debug message.
    """
    # update the snake.
    snake.change_direction(c)
    snake.move()
    code = snake.update(snake.is_eating(apples))

    # if the snake is dead, beep + stop game + change debug message. Otherwise, increment the score.
    if code < Snake.NOTHING:
        curses.beep()
        new_game_state = LOST
        if code == Snake.OUTSIDE:
            new_debug_msg = f"hit walls -> {score}"
        elif code == Snake.SELF_BITE:
            new_debug_msg = f"self_intersect -> {score}"
        else:
            new_debug_msg = None
        return None, new_game_state, new_debug_msg
    else:
        return score + code, None, None


def blit(stdscr, borders, snake, apples, score, game_state, debug, debug_msg, fps):
    """
        Blits all the objects of the game onto the screen.

        Args
        ----
        stdscr : _curses.window
            the screen object.
        borders : list of int 2-uples
            the positions of all the borders elements.
        snake : src.Snake.Snake
            the snake.
        apples : list of src.Apple.Apple instances.
            all the apples in the game.
        score : int
            the current score in the game.
        game_state : int
            the current state of the game.
        debug : bool
            triggers the printing of the debug message.
        debug_msg : str
            the current debug message.
        fps ; int
            the frame rate of the game.

        Returns
        -------
        None
    """
    # erase the screen.
    stdscr.erase()

    # print the borders.
    for y, x in borders:
        stdscr.insch(y, x, ' ', curses.color_pair(WALL))

    # show the entities.
    snake.show(stdscr)
    for apple in apples:
        apple.show(stdscr)

    # print some strings.
    msgs = [
        # f"{snake.trail = }",
        # f"{len(snake.body) = }",
        f"{score = }",
        f"{game_state = }",
    ]
    if debug:
        msgs += [f"{debug_msg = }"]
    h = 0 if snake.get_head()[0] > curses.LINES // 2 else curses.LINES - len(msgs)
    for row, msg in zip(range(len(msgs)), list(map(str, msgs))):
        stdscr.addstr(h + row, 0, msg)

    # refresh and wait.
    stdscr.refresh()
    time.sleep(1 / fps)


def get_user_name(stdscr):
    """
        Gets the username, either by reading the user file or by prompting the user.

        Args
        ----
        stdscr : _curses.window
            the screen object.

        Returns
        -------
        user_name : str
            the username to user during next game.
    """
    # some basic variables.
    user_file = ".user"
    user_name = ''
    prompt = not os.path.exists(user_file)
    msg = "Enter username: (hit Ctrl-G or enter to confirm)"

    # the suer file exists.
    if not prompt:
        # read the file.
        with open(user_file, 'r') as file:
            user_name = file.readlines()
            if len(user_name) != 1:  # if content has strange format, prompt the user.
                prompt = True
                msg = "user file has been corrupted... " + msg
            else:
                user_name = user_name[0].strip()

    # the user needs to be prompted (unknown user or corrupted user file.)
    if prompt:
        while user_name == '':  # do not take empty strings into account.
            user_name = prompt_user(stdscr, msg=msg).strip()
        # save the username in the user file.
        with open(user_file, 'w') as file:
            file.write(user_name)

    return user_name
