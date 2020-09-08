class Board(): 
    layout = list()
    cx = int()
    cy = int()
    sx = int()
    sy = int()
    hist = list()

    def __init__(self):
        self.reset()

    def reset(self):
        self.hist = list()
        self.layout = list(
            [
                [' ', ' ', ' ', 'o', 'o', 'o', ' ', ' ', ' '],
                [' ', ' ', ' ', 'o', 'o', 'o', ' ', ' ', ' '],
                [' ', ' ', ' ', 'o', 'o', 'o', ' ', ' ', ' '],
                ['o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o'],
                ['o', 'o', 'o', 'o', 'x', 'o', 'o', 'o', 'o'],
                ['o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o'],
                [' ', ' ', ' ', 'o', 'o', 'o', ' ', ' ', ' '],
                [' ', ' ', ' ', 'o', 'o', 'o', ' ', ' ', ' '],
                [' ', ' ', ' ', 'o', 'o', 'o', ' ', ' ', ' '],
            ]
        )
        self.cx = 4
        self.cy = 4
        self.sx = 0
        self.sy = 0
    
    def save_state(self):
        copy = list()
        for i in range(0, 9):
            copy.append(list())
            for j in range(0, 9):
                copy[i].append(self.layout[i][j])
        self.hist.append(copy)

    def load_last(self):
        if self.hist:
            lay = self.hist.pop()
            self.layout = lay
    
    def select_cursor(self):
        print('making selection')
        char = self.cursor_char()
        layout = self.layout
        print (char)
        if char == 'x':
            if self.sx or self.sy:
                layout[self.sy][self.sx] = 'x'
            self.sx = self.cx
            self.sy = self.cy
            layout[self.sy][self.sx] = '+'
        elif self.sx or self.sy:
            layout[self.sy][self.sx] = 'x'
            self.sx = 0
            self.sy = 0

    
    def make_move(self, direction):
        print('moving ', end='')
        sx = self.sx
        sy = self.sy

        def deselection():
            print(f'deselecting {sx} {sy}')
            self.layout[sy][sx] = 'x'
            self.save_state()
            self.layout[sy][sx] = 'o'
            self.sx = 0
            self.sy = 0

        try:
            if direction == 'u':
                print('up', end='')
                print(self.layout[sy-2][sx])
                if self.layout[sy-1][sx] == 'o' and self.layout[sy - 2][sx] == 'o' and sy > 1:
                    deselection()
                    self.layout[sy - 1][sx] = 'x'
                    self.layout[sy - 2][sx] = 'x'
            elif direction == 'd':
                print('down', end='')
                if self.layout[sy + 1][sx] == 'o' and self.layout[sy + 2][sx] == 'o' and sy < 7:
                    deselection()
                    self.layout[sy + 1][sx] = 'x'
                    self.layout[sy + 2][sx] = 'x'
            elif direction == 'l':
                print('left', end='')
                if self.layout[sy][sx - 1] == 'o' and self.layout[sy][sx - 2] == 'o' and sx > 1:
                    deselection()
                    self.layout[sy][sx - 1] = 'x'
                    self.layout[sy][sx - 2] = 'x'
            elif direction == 'r':
                print('right', end='')
                if self.layout[sy][sx + 1] == 'o' and self.layout[sy][sx + 2] == 'o' and sx < 7:
                    deselection()
                    self.layout[sy][sx + 1] = 'x'
                    self.layout[sy][sx + 2] = 'x'
        except IndexError as e:
            pass

    def move_cursor(self, direction):
        if direction == 'u':
            if self.layout[self.cy - 1][self.cx] != ' ' and self.cy != 0:
                print('moving cursor up')
                self.cy -= 1
            else:
                print('cant move cursor up')
        elif direction == 'd':
            try:
                if self.layout[self.cy + 1][self.cx] != ' ' and self.cy != 8:
                    print('moving cursor down')
                    self.cy += 1
                else:
                    print('cant move cursor down')
            except Exception as e:
                pass
        elif direction == 'l':
            if self.layout[self.cy][self.cx - 1 ] != ' ' and self.cx != 0:
                print('moving cursor left')
                self.cx -= 1
            else:
                print('cant move cursor left')
        elif direction == 'r':
            try:
                if self.layout[self.cy][self.cx + 1] != ' ' and self.cx != 8:
                    print('moving cursor right')
                    self.cx += 1
                else:
                    print('cant move cursor right')
            except Exception as e:
                pass

    def move(self, direction):
        if self.sx or self.sy:
            self.make_move(direction)
        else:
            self.move_cursor(direction)

    def select(self):
        pass

    def print_board(self):
        print('- - - - - - - - - ')
        print(f'cx{self.cx}cy{self.cy} - sx{self.sx}sy{self.sy} ')
        print('- - - - - - - - - ')
        for row in self.layout:
            for cell in row:
                print(f'{cell} ', end='')
            print()
        print('- - - - - - - - - ')
    
    def cursor_char(self):
        return self.layout[self.cy][self.cx]
