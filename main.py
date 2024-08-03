import pygame
import sys
import time

from define import *
from utils import *
from block import Chessboard
from pygame.locals import *

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('扫雷')
    
    # set the font of word
    font1 = pygame.font.Font('resources/a.TTF', SIZE * 2)
    fwidth, fheight = font1.size('999')
    red = (200, 40, 40)

    # Load and resize the images
    img0 = pygame.image.load('resources/0.bmp').convert()
    img0 = pygame.transform.smoothscale(img0, (SIZE, SIZE))
    img1 = pygame.image.load('resources/1.bmp').convert()
    img1 = pygame.transform.smoothscale(img1, (SIZE, SIZE))
    img2 = pygame.image.load('resources/2.bmp').convert()
    img2 = pygame.transform.smoothscale(img2, (SIZE, SIZE))
    img3 = pygame.image.load('resources/3.bmp').convert()
    img3 = pygame.transform.smoothscale(img3, (SIZE, SIZE))
    img4 = pygame.image.load('resources/4.bmp').convert()
    img4 = pygame.transform.smoothscale(img4, (SIZE, SIZE))
    img5 = pygame.image.load('resources/5.bmp').convert()
    img5 = pygame.transform.smoothscale(img5, (SIZE, SIZE))
    img6 = pygame.image.load('resources/6.bmp').convert()
    img6 = pygame.transform.smoothscale(img6, (SIZE, SIZE))
    img7 = pygame.image.load('resources/7.bmp').convert()
    img7 = pygame.transform.smoothscale(img7, (SIZE, SIZE))
    img8 = pygame.image.load('resources/8.bmp').convert()
    img8 = pygame.transform.smoothscale(img8, (SIZE, SIZE))
    img_blank = pygame.image.load('resources/blank.bmp').convert()
    img_blank = pygame.transform.smoothscale(img_blank, (SIZE, SIZE))
    img_flag = pygame.image.load('resources/flag.bmp').convert()
    img_flag = pygame.transform.smoothscale(img_flag, (SIZE, SIZE))
    img_ask = pygame.image.load('resources/ask.bmp').convert()
    img_ask = pygame.transform.smoothscale(img_ask, (SIZE, SIZE))
    img_mine = pygame.image.load('resources/mine.bmp').convert()
    img_mine = pygame.transform.smoothscale(img_mine, (SIZE, SIZE))
    img_blood = pygame.image.load('resources/blood.bmp').convert()
    img_blood = pygame.transform.smoothscale(img_blood, (SIZE, SIZE))
    img_error = pygame.image.load('resources/error.bmp').convert()
    img_error = pygame.transform.smoothscale(img_error, (SIZE, SIZE))
    face_size = int(SIZE * 1.25)
    img_face_fail = pygame.image.load('resources/face_fail.bmp').convert()
    img_face_fail = pygame.transform.smoothscale(img_face_fail, (face_size, face_size))
    img_face_normal = pygame.image.load('resources/face_normal.bmp').convert()
    img_face_normal = pygame.transform.smoothscale(img_face_normal, (face_size, face_size))
    img_face_success = pygame.image.load('resources/face_success.bmp').convert()
    img_face_success = pygame.transform.smoothscale(img_face_success, (face_size, face_size))
    face_pos_x = (SCREEN_WIDTH - face_size) // 2
    face_pos_y = (SIZE * 2 - face_size) // 2
    img_dict = {0: img0, 1: img1, 2: img2, 3: img3, 4: img4, 5: img5, 6: img6, 7: img7, 8: img8}
    bgcolor = (225, 225, 225)
    block = Chessboard()
    game_status = READIED
    
    # Start time
    start_time = None
    # cost time
    elapsed_time = 0
    while True:
        screen.fill(bgcolor)
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                x = mouse_x // SIZE
                y = mouse_y // SIZE - 2
                b1, b2, b3 = pygame.mouse.get_pressed()
                if game_status == STARTED:
                    # Click both left and right button
                    if b1 and b3:
                        mine = block.getmine(x, y)
                        if mine.status == OPENED:
                            if not block.double_mouse_button_down(x, y):
                                game_status = OVER
            elif event.type == MOUSEBUTTONUP:
                if y < 0:
                    if face_pos_x <= mouse_x <= face_pos_x + face_size \
                            and face_pos_y <= mouse_y <= face_pos_y + face_size:
                        game_status = READIED
                        block = Chessboard()
                        start_time = time.time()
                        elapsed_time = 0
                        continue
                if game_status == READIED:
                    game_status = STARTED
                    start_time = time.time()
                    elapsed_time = 0
                if game_status == STARTED:
                    mine = block.getmine(x, y)
                    # Click left button
                    if b1 and not b3:
                        if mine.status == NORMAL:
                            if not block.open_mine(x, y):
                                game_status = OVER
                    # Click right button
                    elif not b1 and b3:
                        if mine.status == NORMAL:
                            mine.status = FLAG
                        elif mine.status == FLAG:
                            mine.status = ASK
                        elif mine.status == ASK:
                            mine.status = NORMAL
                    elif b1 and b3:
                        if mine.status == DOUBLE:
                            block.double_mouse_button_up(x, y)
        flag_count = 0
        opened_count = 0
        for row in block.block:
            for mine in row:
                pos = (mine.x * SIZE, (mine.y + 2) * SIZE)
                if mine.status == OPENED:
                    screen.blit(img_dict[mine.around_mine_count], pos)
                    opened_count += 1
                elif mine.status == DOUBLE:
                    screen.blit(img_dict[mine.around_mine_count], pos)
                elif mine.status == BOMB:
                    screen.blit(img_blood, pos)
                elif mine.status == FLAG:
                    screen.blit(img_flag, pos)
                    flag_count += 1
                elif mine.status == ASK:
                    screen.blit(img_ask, pos)
                elif mine.status == HINT:
                    screen.blit(img0, pos)
                elif game_status == OVER and mine.value:
                    screen.blit(img_mine, pos)
                elif mine.value == 0 and mine.status == FLAG:
                    screen.blit(img_error, pos)
                elif mine.status == NORMAL:
                    screen.blit(img_blank, pos)
        print_text(screen, font1, 30, (SIZE * 2 - fheight) // 2 - 2, '%02d' % (MINE_COUNT - flag_count), red)
        if game_status == STARTED:
            elapsed_time = int(time.time() - start_time)
        print_text(screen, font1, SCREEN_WIDTH - fwidth - 30, (SIZE * 2 - fheight) // 2 - 2, '%03d' % elapsed_time, red)
        if flag_count + opened_count == BLOCK_WIDTH * BLOCK_HEIGHT:
            game_status = WIN
        if game_status == OVER:
            screen.blit(img_face_fail, (face_pos_x, face_pos_y))
        elif game_status == WIN:
            screen.blit(img_face_success, (face_pos_x, face_pos_y))
        else:
            screen.blit(img_face_normal, (face_pos_x, face_pos_y))
        pygame.display.update()

if __name__ == '__main__':
    main()
