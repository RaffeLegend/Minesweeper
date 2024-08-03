from define import *

# return the coordinate of (x, y)
def _get_around(x, y):
    return [(i, j) for i in range(max(0, x - 1), min(BLOCK_WIDTH - 1, x + 1) + 1)
            for j in range(max(0, y - 1), min(BLOCK_HEIGHT - 1, y + 1) + 1) if i != x or j != y]

# width of game screen
SCREEN_WIDTH = BLOCK_WIDTH * SIZE
# height of game screen
SCREEN_HEIGHT = (BLOCK_HEIGHT + 2) * SIZE

def print_text(screen, font, x, y, text, fcolor=(255, 255, 255)):
    imgText = font.render(text, True, fcolor)
    screen.blit(imgText, (x, y))
