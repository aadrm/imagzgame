import pygame
import random
from board import Board

WIDTH = 800
HEIGHT = 800
FPS = 30
TITLE = "Hard game from Imagzle"

#define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (155,30,33)
GREEN = (0, 255, 0) 
BLUE = (0, 120, 255) 
YELLOW = (255, 255, 98)
PURPLE = (255, 0, 255)
ORANGE = (240,150,30)
ORANGE_LIGHT = (255,180,40)
# initialize pygame and create window

pygame.init()
# pygame.mixer.init()
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

all_sprites = pygame.sprite.Group()

# board class
tile_size = HEIGHT / 9
board = Board()


class Tile(pygame.sprite.Sprite):
    px = 0
    py = 0
    def __init__(self, px, py):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((tile_size + 1, tile_size + 1))
        self.image.fill((120, 120, 120))
        self.rect = self.image.get_rect()
        self.px = px
        self.py = py
        posx = px * tile_size + tile_size * .5
        posy = py * tile_size + tile_size * .5
        self.rect.center = (int(posx), int(posy))

    def update(self):

        char = board.layout[self.py][self.px]
        # reset sprite
        self.image.fill(ORANGE)
        # show cursor position:
        if board.cx == self.px and board.cy == self.py:
            pygame.draw.circle(self.image, (ORANGE_LIGHT), (int(tile_size / 2), int(tile_size / 2)), int(tile_size / 2))

        if char == 'o':
            pygame.draw.circle(self.image, BLUE, (int(tile_size / 2), int(tile_size / 2)), int(tile_size / 3))
        elif char == 'x':
            pygame.draw.circle(self.image, RED, (int(tile_size / 2), int(tile_size / 2)), int(tile_size / 4))
        elif char == '+':
            pygame.draw.circle(self.image, YELLOW, (int(tile_size / 2), int(tile_size / 2)), int(tile_size / 4))
        


tiles = list()

# create tiles

for i in range(0, 9):
    tiles.append(list())
    for j in range(0, 9):
        tiles[i].append(Tile(i, j)) 
        all_sprites.add(tiles[i][j])

# game loop
running = True
board.print_board()
game_stage = 0
while running:
    # Keep loop runnnig at the right speed
    clock.tick(FPS)
    # Process input
    for event in pygame.event.get():
        # check for closing the window
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            print ('keypress')
            if event.key == pygame.K_UP:
                board.move('u')
            elif event.key == pygame.K_DOWN:
                board.move('d')
            elif event.key == pygame.K_LEFT:
                board.move('l')
            elif event.key == pygame.K_RIGHT:
                board.move('r')

            elif event.key == pygame.K_SPACE:
                board.select_cursor()

            elif event.key == pygame.K_r:
                board.reset()
            
            elif event.key == pygame.K_b:
                board.load_last()
            
            board.print_board()
        
    # Update
    all_sprites.update()
    # Draw
    screen.fill((255, 255, 255))
    all_sprites.draw(screen)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()