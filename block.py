import random

from mine import Mine
from define import *
from utils import _get_around

#define chessboard
class Chessboard:
    def __init__(self):
        self._block = [[Mine(i, j) for i in range(BLOCK_WIDTH)] for j in range(BLOCK_HEIGHT)]
        # prepare mines
        for i in random.sample(range(BLOCK_WIDTH * BLOCK_HEIGHT), MINE_COUNT):
            self._block[i // BLOCK_WIDTH][i % BLOCK_WIDTH].value = 1
    def get_block(self):
        return self._block
    block = property(fget=get_block)
    def getmine(self, x, y):
        return self._block[y][x]
    def open_mine(self, x, y):
        # touch mines
        if self._block[y][x].value:
            self._block[y][x].status = BOMB
            return False
        # update the status of mine as opened
        self._block[y][x].status = OPENED
        around = _get_around(x, y)
        _sum = 0
        for i, j in around:
            if self._block[j][i].value:
                _sum += 1
        self._block[y][x].around_mine_count = _sum
        # 如果周围没有雷，那么将周围 8 个未中未点开的递归算一遍
        if _sum == 0:
            for i, j in around:
                if self._block[j][i].around_mine_count == -1:
                    self.open_mine(i, j)
        return True
    def double_mouse_button_down(self, x, y):
        if self._block[y][x].around_mine_count == 0:
            return True
        self._block[y][x].status = DOUBLE
        around = _get_around(x, y)
        # the number of the flagged mine surround
        sumflag = 0
        for i, j in _get_around(x, y):
            if self._block[j][i].status == FLAG:
                sumflag += 1
        # all the mines surroud are flagged
        result = True
        if sumflag == self._block[y][x].around_mine_count:
            for i, j in around:
                if self._block[j][i].status == NORMAL:
                    if not self.open_mine(i, j):
                        result = False
        else:
            for i, j in around:
                if self._block[j][i].status == NORMAL:
                    self._block[j][i].status = HINT
        return result
    def double_mouse_button_up(self, x, y):
        self._block[y][x].status = OPENED
        for i, j in _get_around(x, y):
            if self._block[j][i].status == HINT:
                self._block[j][i].status = NORMAL
