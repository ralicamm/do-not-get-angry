import pygame
import math
import time


out = [[125, 125], [475, 125], [125, 475], [475, 475]]
places = [[0, -40], [-40, 0], [0, 40], [40, 0]]
img_place = 13

start_points = [(76, 268),(332, 76),(268, 524),(524, 332)]
yellow_start_pos = (start_points[0][0] - img_place, start_points[0][1] - img_place)
blue_start_pos = (start_points[1][0] - img_place, start_points[1][1] - img_place)
green_start_pos = (start_points[2][0] - img_place, start_points[2][1] - img_place)
red_start_pos = (start_points[3][0] - img_place, start_points[3][1] - img_place)


class Player(pygame.sprite.Sprite):
    def __init__(self, group, color_num):
        super(Player, self).__init__(group)
        self.image = pygame.image.load(self.get_color_img(color_num))
        self.color = color_num
        self.all_out = True
        self.have_out = True
        self.score = 0
        self.pieces = pygame.sprite.Group()
        
        for i in range(4):
            piece = pygame.sprite.Sprite(self.pieces)
            piece.image = self.image
            piece.rect = pygame.Rect(
                (out[self.color][0] + places[i][0] - img_place,
                out[self.color][1] + places[i][1] - img_place),
                self.image.get_size())
            piece.pos = 0
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


    def is_point_out(self, x, y):
        for i in range(4):
            if math.sqrt((out[i][0] - x) ** 2 + (out[i][1] - y) ** 2) <= 80:
                return True
        return False

    def get_color_name(self):
        return {
            0: 'Yellow',
            1: 'Blue',
            2: 'Green',
            3: 'Red',
            }.get(self.color)

    def get_color_img(self, color_num):
        return {
            0: 'yellow.png',
            1: 'blue.png',
            2: 'green.png',
            3: 'red.png',
            }.get(color_num, 'red.png')
    
    def get_start_pos(self):
        return {
            0: yellow_start_pos,
            1: blue_start_pos,
            2: green_start_pos,
            3: red_start_pos,
            }.get(self.color)
                              
                
