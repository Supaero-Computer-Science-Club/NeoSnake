import curses

_directions = {
    curses.KEY_UP: (-1, 0),
    curses.KEY_DOWN: (1, 0),
    curses.KEY_LEFT: (0, -1),
    curses.KEY_RIGHT: (0, 1)
}

_corners = {
    "dr": 4194410,
    "ur": 4194411,
    "ul": 4194412,
    "dl": 4194413,
}


class Snake:
    def __init__(self, y, x, h, w):
        head = (y + (y + h) // 2, x + (x + w) // 2)
        self.body = [head]
        tmp = [tuple(map(sum, zip(head, (0, i)))) for i in range(1, 2)]
        self.body += tmp
        self.tokens = ['@'] + ['-'] * len(tmp)

        self.dir = curses.KEY_LEFT
        self.turned = ''

        self.trail = []
        self.score = 0

        self.scene = y, x, h, w

    def change_direction(self, dir):
        if (dir in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]
                and not (self.dir == curses.KEY_UP and dir == curses.KEY_DOWN)
                and not (self.dir == curses.KEY_DOWN and dir == curses.KEY_UP)
                and not (self.dir == curses.KEY_RIGHT and dir == curses.KEY_LEFT)
                and not (self.dir == curses.KEY_LEFT and dir == curses.KEY_RIGHT)):
            if dir != self.dir:
                if self.dir == curses.KEY_RIGHT and dir == curses.KEY_UP:
                    self.turned = _corners["dr"]
                elif self.dir == curses.KEY_RIGHT and dir == curses.KEY_DOWN:
                    self.turned = _corners["ur"]

                elif self.dir == curses.KEY_UP and dir == curses.KEY_RIGHT:
                    self.turned = _corners["ul"]
                elif self.dir == curses.KEY_UP and dir == curses.KEY_LEFT:
                    self.turned = _corners["ur"]

                elif self.dir == curses.KEY_LEFT and dir == curses.KEY_UP:
                    self.turned = _corners["dl"]
                elif self.dir == curses.KEY_LEFT and dir == curses.KEY_DOWN:
                    self.turned = _corners["ul"]

                elif self.dir == curses.KEY_DOWN and dir == curses.KEY_LEFT:
                    self.turned = _corners["dr"]
                elif self.dir == curses.KEY_DOWN and dir == curses.KEY_RIGHT:
                    self.turned = _corners["dl"]

            self.dir = dir

    def move(self):
        self.body.pop()
        self.tokens.pop()
        new_head = self.body[0][0] + _directions[self.dir][0], self.body[0][1] + _directions[self.dir][1]
        self.body.insert(0, new_head)
        if self.turned:
            self.tokens.insert(1, self.turned)
        elif self.dir in [curses.KEY_UP, curses.KEY_DOWN]:
            self.tokens.insert(1, '|')
        elif self.dir in [curses.KEY_LEFT, curses.KEY_RIGHT]:
            self.tokens.insert(1, '-')
        if self.trail:
            self.body.append(self.trail.pop())
            self.tokens.append('.')

        self.turned = ''

    def is_eating(self, apple):
        eating_apple = self.body[0] == apple.pos
        if eating_apple:
            self.score += 1
            apple.spawn(*self.scene)
        return eating_apple

    def head(self):
        return self.body[0]

    def inside(self, y, x, h, w):
        return (y < self.body[0][0] < y + h - 1) and (x < self.body[0][1] < x + w - 1)

    def self_intersect(self):
        return sum([self.head() == part for part in self.body[1:]])

    def update(self, eating_apple, ):
        if eating_apple:
            self.trail += [self.body[-1]] * 10

        if not self.inside(*self.scene):
            return 1
            # raise Warning(f"hit walls -> {self.score}")

        if self.self_intersect():
            return 2
            # raise Warning(f"self_intersect -> {self.score}")

        return 0

    def show(self, stdscr):
        for i, part in enumerate(self.body[1:]):
            stdscr.addch(*part, self.tokens[i + 1])

        if self.inside(*self.scene):
            stdscr.addstr(*self.body[0], '@')

        msgs = [f"trail: {self.trail}",
                f" body: {len(self.body)}",
                f"score: {self.score}"]
        h = 0 if self.head()[0] > curses.LINES // 2 else curses.LINES - 1 - len(msgs)
        for row, msg in zip(range(len(msgs)), list(map(str, msgs))):
            stdscr.addstr(h + row, 0, msg)
