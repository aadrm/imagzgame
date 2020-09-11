from board import Board

game = Board()

# game.print_board()
run = True
while not(game.victory):
    game.auto_play()
else:
    print('you win')

