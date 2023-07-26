import pygame

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH//COLS

# RED = (255, 0, 0)
# WHITE = (255, 255, 255)
BLACK_SQUARES = (125, 135, 150)  # ciemne pola
WHITE_PIECES = (242, 242, 242) # białe pionki
BLACK_PIECES = (33, 33, 33) # nigga pionki
LIGHT_SQUARES = (232, 235, 239) # jasne pola


BLUE = (0, 0, 255)
GREY = (128, 128, 128)

CROWN = pygame.transform.scale(pygame.image.load('assets/crown.png'), (44, 25))


