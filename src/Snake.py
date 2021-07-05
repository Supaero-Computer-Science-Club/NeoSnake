import curses
import random

_directions = {
    curses.KEY_UP: (-1, 0),
    curses.KEY_DOWN: (1, 0),
    curses.KEY_LEFT: (0, -1),
    curses.KEY_RIGHT: (0, 1),
}

_corners = {
    "dr": 4194410,
    "ur": 4194411,
    "ul": 4194412,
    "dl": 4194413,
}


class Snake:
    """ The snake in the game of snake."""

    NOTHING = 0
    SELF_BITE = -1
    OUTSIDE = -2

    def __init__(self, swiftness):
        # the body and the assets (resp. the positions of the parts and the assets used for rendering)
        self.body, self.assets = None, None
        # a cache of the scene used in the game.
        self.scene = None
        # the direction in which the snake is going and the new asset to add to the snake.
        self.dir, self.neck_asset = None, None

        # a list containing parts to add to the snake, allows better animation.
        self.trail = None

        # the swiftness of the snake, inversely proportional to the rate at which the snake moves.
        # the number of life steps that the snake experienced.
        self.swiftness = swiftness
        self.life_step = None

    def spawn(self, y, x, h, w, init_length=3):
        """
            Spawns the apple inside the game area.

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
            init_length : int >= 0, optional
                the initial length of the snake.

            Returns
            -------
            None
        """
        # cache the scene.
        self.scene = y, x, h, w

        # spawn in the middle of the scene, with random direction.
        head = (y + h // 2, x + w // 2)
        self.body = [head]
        self.dir = random.sample([curses.KEY_LEFT, curses.KEY_DOWN, curses.KEY_UP, curses.KEY_RIGHT], k=1)[0]

        # build the initial body in the opposite direction.
        if self.dir == curses.KEY_LEFT:
            tmp = [tuple(map(sum, zip(head, (0, i + 1)))) for i in range(init_length)]
        elif self.dir == curses.KEY_RIGHT:
            tmp = [tuple(map(sum, zip(head, (0, -i - 1)))) for i in range(init_length)]
        elif self.dir == curses.KEY_UP:
            tmp = [tuple(map(sum, zip(head, (i + 1, 0)))) for i in range(init_length)]
        else:
            tmp = [tuple(map(sum, zip(head, (-i - 1, 0)))) for i in range(init_length)]
        self.body += tmp

        # the assets are simply the head plus the right amount of body parts.
        self.assets = ['@'] + ['|' if self.dir in [curses.KEY_UP, curses.KEY_DOWN] else '-'] * len(tmp)

        # reset the trail of the snake.
        self.trail = []

        # reset the number of life steps.
        self.life_step = 0

    def change_direction(self, new_dir):
        """
            Changes the direction of the snake if it is different and compatible with current one,
            e.g. can not go from up to down without twisting the neck of the snake...

            Args
            ----
            new_dir : int
                the new direction that the player just gave as an input.

            Returns
            -------
            None
        """
        # useless if directions are the same.
        if new_dir != self.dir:
            # the snake turns only if:
            #  - the new direction is an arrow (1st line)
            #  - the player does not query a complete direction flip (4 last lines)
            if (new_dir in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]
                    and not (self.dir == curses.KEY_UP and new_dir == curses.KEY_DOWN)
                    and not (self.dir == curses.KEY_DOWN and new_dir == curses.KEY_UP)
                    and not (self.dir == curses.KEY_RIGHT and new_dir == curses.KEY_LEFT)
                    and not (self.dir == curses.KEY_LEFT and new_dir == curses.KEY_RIGHT)):
                # check all possible combinations to determine the corner to display.
                if self.dir == curses.KEY_RIGHT and new_dir == curses.KEY_UP:
                    self.neck_asset = _corners["dr"]  # down+right corner.
                elif self.dir == curses.KEY_RIGHT and new_dir == curses.KEY_DOWN:
                    self.neck_asset = _corners["ur"]  # up+right corner.

                elif self.dir == curses.KEY_UP and new_dir == curses.KEY_RIGHT:
                    self.neck_asset = _corners["ul"]  # up+left corner.
                elif self.dir == curses.KEY_UP and new_dir == curses.KEY_LEFT:
                    self.neck_asset = _corners["ur"]  # up+right corner.

                elif self.dir == curses.KEY_LEFT and new_dir == curses.KEY_UP:
                    self.neck_asset = _corners["dl"]  # down+left corner.
                elif self.dir == curses.KEY_LEFT and new_dir == curses.KEY_DOWN:
                    self.neck_asset = _corners["ul"]  # up+left corner.

                elif self.dir == curses.KEY_DOWN and new_dir == curses.KEY_LEFT:
                    self.neck_asset = _corners["dr"]  # down+right corner.
                elif self.dir == curses.KEY_DOWN and new_dir == curses.KEY_RIGHT:
                    self.neck_asset = _corners["dl"]  # down+left corner.

                self.dir = new_dir

                # return immediately.
                return

        # here, no changes or going in a straight line -> update the asset accordingly.
        if self.dir in [curses.KEY_UP, curses.KEY_DOWN]:
            self.neck_asset = '|'
        elif self.dir in [curses.KEY_LEFT, curses.KEY_RIGHT]:
            self.neck_asset = '-'
        else:
            self.neck_asset = '*'

    def move(self):
        """
            Moves the snake around the scene according to the direction.

            Args
            ----

            Returns
            -------
            None
        """
        self.life_step += 1
        if self.life_step % self.swiftness == 0:
            # pop the head.
            self.body.pop()
            self.assets.pop()

            # compute and insert the new head and the neck asset.
            new_head = self.body[0][0] + _directions[self.dir][0], self.body[0][1] + _directions[self.dir][1]
            self.body.insert(0, new_head)
            self.assets.insert(1, self.neck_asset)

        # complete the snake with its trail.
        if self.trail:
            self.body.append(self.trail.pop())
            self.assets.append('.')

    def is_eating(self, apples):
        """
            Checks if the snake ate any of the apples in the scene.

            Args
            ----
            apples : list of Apple instances
                all the apples to check.

            Returns
            -------
            count : int
                the number of apples that the snake ate during current frame.
        """
        count = 0
        for apple in apples:
            eaten = self.body[0] == apple.pos  # apple eaten?
            if eaten:
                curses.beep()  # make a sound.
                apple.spawn(*self.scene)  # respawn the eaten apple.
            count += eaten
        return count

    def get_head(self):
        """ Gives the head (int x int) of the snake. """
        return self.body[0]

    def inside(self, y, x, h, w):
        """ Checks whether the head of the snake is strictly inside the scene. """
        return (y <= self.body[0][0] < y + h) and (x <= self.body[0][1] < x + w)

    def self_intersect(self):
        """ Returns a boolean telling if the snake bit its own tail. """
        # count the number of self intersections between the head and any of the body parts.
        return sum([self.body[0] == part for part in self.body[1:]])

    def update(self, eaten_apples, trail_length=10):
        """
            Updates the snake.

            Args
            ----
            eaten_apples : int
                the number of apples that were eaten during current frame.
            trail_length : int >= 1, optional
                the number of body parts to append to the snake when an apple is eaten. Usually, depends on the
                difficulty.

            Returns
            -------
            score or error code: int
                the score performed or an error code.
        """
        if eaten_apples:
            self.trail += [self.body[-1]] * trail_length  # copy the tail a given amount of times, in place.
            return eaten_apples

        if not self.inside(*self.scene):
            return Snake.OUTSIDE

        if self.self_intersect():
            return Snake.SELF_BITE

        return Snake.NOTHING

    def show(self, stdscr):
        """
            Displays the snake on the screen.

            Args
            ----
            stdscr : _curses.window
                the window on which to display the object.

            Returns
            -------
            None
        """
        # show the parts with the right assets.
        for i, part in enumerate(self.body[1:]):
            stdscr.addch(*part, self.assets[i + 1])

        # show the head only if inside the scene.
        if self.inside(*self.scene):
            stdscr.addstr(*self.body[0], '@')
