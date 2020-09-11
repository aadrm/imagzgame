class Board(): 
    layout = list()
    cx = int()
    cy = int()
    sx = int()
    sy = int()
    hist = list()
    move_hist = list()
    stuck_counter = 0
    move_counter = 0
    reached_end_counter = 0
    same_solution_counter = 0
    reached_end = False
    victory = False

    selectable_map = list()
    correct = list(
        [
            [' ', ' ', ' ', 'x', 'x', 'x', ' ', ' ', ' '],
            [' ', ' ', ' ', 'x', 'x', 'x', ' ', ' ', ' '],
            [' ', ' ', ' ', 'x', 'x', 'x', ' ', ' ', ' '],
            ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
            ['x', 'x', 'x', 'x', 'o', 'x', 'x', 'x', 'x'],
            ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
            [' ', ' ', ' ', 'x', 'x', 'x', ' ', ' ', ' '],
            [' ', ' ', ' ', 'x', 'x', 'x', ' ', ' ', ' '],
            [' ', ' ', ' ', 'x', 'x', 'x', ' ', ' ', ' '],

        ]
    )



    def __init__(self):
        self.reset()

    def reset(self):
        self.hist = list()
        self.move_hist = list()
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
        selectable_map = list()
        self.find_selectable()
    
    def save_state(self):
        copy = list()
        for i in range(0, 9):
            copy.append(list())
            for j in range(0, 9):
                copy[i].append(self.layout[i][j])
        # self.hist.append(copy)

    # def load_last(self):
    #     if self.hist:
    #         lay = self.hist.pop()
    #         self.layout = lay
    
    def undo_move(self):
        if self.move_hist:
            move = self.move_hist.pop()
            move_x = move[0][0]
            move_y = move[0][1]
            direction = move[1]
            self.layout[move_y][move_x] = 'x'
            if direction == 'u':
                self.layout[move_y - 1][move_x], self.layout[move_y - 2][move_x] = 'o', 'o'
            if direction == 'd':
                self.layout[move_y + 1][move_x], self.layout[move_y + 2][move_x] = 'o', 'o'
            if direction == 'l':
                self.layout[move_y][move_x - 1], self.layout[move_y][move_x - 2] = 'o', 'o'
            if direction == 'r':
                self.layout[move_y][move_x + 1], self.layout[move_y][move_x + 2] = 'o', 'o'


    
    def select_cursor(self):
        # print('making selection')
        char = self.cursor_char()
        layout = self.layout
        # print (char)
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
        # print('moving ', end='')
        sx = self.sx
        sy = self.sy
        valid_moves = self.check_valid_moves(sx, sy)

        def after_move():
            # print(f'deselecting {sx} {sy}')
            self.layout[sy][sx] = 'x'
            # self.save_state()
            self.layout[sy][sx] = 'o'
            self.sy = 0
            self.sx = 0
        
        if direction:
            self.move_hist.append([(self.sx, self.sy), direction])
        try:
            if direction == 'u' and 'u' in valid_moves:
                # print('up', end='')
                # print(self.layout[sy-2][sx])
                after_move()
                self.layout[sy - 1][sx] = 'x'
                self.layout[sy - 2][sx] = 'x'
                self.find_selectable()
            elif direction == 'd' and 'd' in valid_moves:
                # print('down', end='')
                after_move()
                self.layout[sy + 1][sx] = 'x'
                self.layout[sy + 2][sx] = 'x'
                self.find_selectable()
            
            elif direction == 'l' and 'l' in valid_moves:
                # print('left', end='')
                after_move()
                self.layout[sy][sx - 1] = 'x'
                self.layout[sy][sx - 2] = 'x'
                self.find_selectable()
            elif direction == 'r' and 'r' in valid_moves:
                # print('right', end='')
                after_move()
                self.layout[sy][sx + 1] = 'x'
                self.layout[sy][sx + 2] = 'x'
                self.find_selectable()
        except IndexError as e:
            pass

    def move_cursor(self, direction):
        if direction == 'u':
            if self.layout[self.cy - 1][self.cx] != ' ' and self.cy != 0:
                # print('moving cursor up')
                self.cy -= 1
            # else:
                # print('cant move cursor up')
        elif direction == 'd':
            try:
                if self.layout[self.cy + 1][self.cx] != ' ' and self.cy != 8:
                    # print('moving cursor down')
                    self.cy += 1
                # else:
                    # print('cant move cursor down')
            except Exception as e:
                pass
        elif direction == 'l':
            if self.layout[self.cy][self.cx - 1 ] != ' ' and self.cx != 0:
                # print('moving cursor left')
                self.cx -= 1
            # else:
                # print('cant move cursor left')
        elif direction == 'r':
            try:
                if self.layout[self.cy][self.cx + 1] != ' ' and self.cx != 8:
                    # print('moving cursor right')
                    self.cx += 1
                # else:
                    # print('cant move cursor right')
            except Exception as e:
                pass

    def move(self, direction):
        if self.sx or self.sy:
            self.make_move(direction)
        else:
            self.move_cursor(direction)

    def print_board(self):
        # print('- - - - - - - - - ')
        # print(f'cx{self.cx}cy{self.cy} - sx{self.sx}sy{self.sy} ')
        # print('- - - - - - - - - ')
        for row in self.layout:
            for cell in row:
                print(f'{cell} ', end='')
            # print()
        # print('- - - - - - - - - ')
    
    def cursor_char(self):
        return self.layout[self.cy][self.cx]

    # solver
    
    def find_selectable(self):
        selectable = list()
        self.print_board()
        for i in range(0, 9):
            for j in range(0, 9):
                if self.layout[i][j] == 'x':
                    valid_moves = self.check_valid_moves(j, i)
                    if valid_moves:
                        selectable.append([(i, j), valid_moves])
                    # selectable[(i, j)] = valid_moves
        if selectable:
            self.selectable_map.append(selectable)   
            print(f'added selectable map {selectable}')

    def check_valid_moves(self, x, y):
        valid_moves = list()
        # print (self.layout[y][x])
        if self.layout[y][x] in ('+', 'x'):
            try:
                if self.layout[y-1][x] == 'o' and self.layout[y - 2][x] == 'o' and y > 1:
                    valid_moves.append('u')
                if self.layout[y + 1][x] == 'o' and self.layout[y + 2][x] == 'o' and y < 7:
                    valid_moves.append('d')
                if self.layout[y][x - 1] == 'o' and self.layout[y][x - 2] == 'o' and x > 1:
                    valid_moves.append('l')
                if self.layout[y][x + 1] == 'o' and self.layout[y][x + 2] == 'o' and x < 7:
                    valid_moves.append('r')
            except IndexError as e:
                pass
        return valid_moves
    
    def auto_move_cursor(self):
        if self.selectable_map[-1][-1]:
            # print(self.selectable_map[-1][-1][0])
            cursor_coordinates = self.selectable_map[-1][-1][0]
            self.cx = cursor_coordinates[1]
            self.cy = cursor_coordinates[0]
            
    def decide_move_direction(self):
        moves = self.selectable_map[-1][-1][1]
        if moves: 
            direction = moves.pop()
            # print(f'move direction: {direction}')
            return direction 
        # else:
            # print('no move possible')

    def auto_play(self):
        if self.layout != self.correct:
            self.move_counter += 1
            self.auto_move_cursor()
            self.select_cursor()
            move_direction = self.decide_move_direction()
            if move_direction:
                self.stuck_counter = 0
                self.move(move_direction)
                print(self.move_hist)
                self.reached_end = False
            else:
                if not(self.reached_end):
                    self.reached_end_counter += 1
                    # if self.move_hist in self.hist:
                    #     self.same_solution_counter += 1
                    # else:
                    #     self.hist.append(list(self.move_hist))
                    # print('--history--')
                    # print(self.hist)
                    # print('--history--')
                self.reached_end = True
                self.selectable_map[-1].pop()
                if not(self.selectable_map[-1]):
                    self.selectable_map.pop()
                self.undo_move()
            print(f'moves {self.move_counter}')
            print(f'endin {self.reached_end_counter}')
            # print(f'repea {self.same_solution_counter}')
        else:
            self.victory = True
        
        # if self.stuck_counter > 10:
        #     return False
        #     print(self.selectable_map)
        #     quit()
