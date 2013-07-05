import pygame
import math
import time


class Player(pygame.sprite.Sprite):
    START_POINTS = [(76, 268), (332, 76), (268, 524), (524, 332)]
    OUT = [[125, 125], [475, 125], [125, 475], [475, 475]]
    PLACES = [[0, -40], [-40, 0], [0, 40], [40, 0]]

    IMG_PLACE = 13

    def __init__(self, group, color_num):
        super(Player, self).__init__(group)
        self.image = pygame.image.load(self.get_color_img(color_num))
        self.color = color_num
        self.all_out = True
        self.have_out = True
        self.score = 0
        self.board_pos = 0
        self.pieces = pygame.sprite.Group()

        for i in range(4):
            piece = pygame.sprite.Sprite(self.pieces)
            piece.image = self.image
            piece.rect = pygame.Rect(
                (self.OUT[self.color][0] + self.PLACES[i][0] - self.IMG_PLACE,
                 self.OUT[self.color][1] + self.PLACES[i][1] - self.IMG_PLACE),
                self.image.get_size())
            piece.pos = 0
            piece.close_in_front = 0
            piece.close_behind = 0
            self.rect = piece.rect

        group.add(self.pieces)

    def update(self):
        x, y = pygame.mouse.get_pos()
        is_out = self.is_point_out(x, y)

        self.all_out = True
        self.have_out = False
        self.score = 0
        for piece in self.pieces:
            if piece.pos != 0:
                self.all_out = False
            else:
                self.have_out = True

            if piece.pos == 62:
                self.score += 1

            if piece.pos > 0 and piece.pos < 57:
                piece.board_pos = self.get_board_pos(piece)
            else:
                piece.board_pos = 0

    def is_point_out(self, x, y):
        for i in range(4):
            if math.sqrt((self.OUT[i][0] - x) ** 2 +
                         (self.OUT[i][1] - y) ** 2) <= 80:
                return True
        return False

    def get_board_pos(self, p):
        if self.color == 0 and p.pos < 29:
            return p.pos + 28
        elif self.color == 0:
            return p.pos - 28
        if (self.color == 1 and p.pos < 15):
            return p.pos + 42
        elif self.color == 1:
            return p.pos - 14
        if (self.color == 2 and p.pos < 43):
            return p.pos + 14
        elif self.color == 2:
            return p.pos - 42
        if self.color == 3:
            return p.pos

    def get_color_name(self):
        return {
            0: 'Yellow',
            1: 'Blue',
            2: 'Green',
            3: 'Red'}.get(self.color)

    def get_color_img(self, color_num):
        return {
            0: 'yellow.png',
            1: 'blue.png',
            2: 'green.png',
            3: 'red.png'}.get(color_num, 'red.png')

    def get_start_pos(self):
        return {
            0: (self.START_POINTS[0][0] - self.IMG_PLACE,
                self.START_POINTS[0][1] - self.IMG_PLACE),
            1: (self.START_POINTS[1][0] - self.IMG_PLACE,
                self.START_POINTS[1][1] - self.IMG_PLACE),
            2: (self.START_POINTS[2][0] - self.IMG_PLACE,
                self.START_POINTS[2][1] - self.IMG_PLACE),
            3: (self.START_POINTS[3][0] - self.IMG_PLACE,
                self.START_POINTS[3][1] - self.IMG_PLACE)}.get(self.color)
