import curses

from src.utils import log


class CustomError(Exception):
    pass


# class CustomError(Exception):
#     """Exception raised for errors in the input salary.
#
#     Attributes:
#         salary -- input salary which caused the error
#         message -- explanation of the error
#     """
#
#     def __init__(self, salary, message="Salary is not in (5000, 15000) range"):
#         self.salary = salary
#         self.message = message
#         super().__init__(self.message)
#
#     def __str__(self):
#         return f'{self.salary} -> {self.message}'

def curses_wrapper(func):
    def wrapper(*args, **kwargs):
        log("init")
        stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        stdscr.keypad(True)
        curses.start_color()
        try:
            log("main")
            func(stdscr=stdscr, *args, **kwargs)
        finally:
            log("quit")
            curses.nocbreak()
            stdscr.keypad(False)
            curses.echo()
            curses.endwin()

    return wrapper


def error_handler_wrapper(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except CustomError as ce:
            log("CustomError")
            print(ce)
        except KeyboardInterrupt:
            log("KeyboardInterrupt")
            pass

    return wrapper
