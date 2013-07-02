import pygame
import time
from random import *
from player import *

clock = pygame.time.Clock()


background =  (164, 211, 238) #(153, 204, 255) #(126, 192, 238)
black = (0, 0, 0)
white = (255, 255, 255)
blue  = (0, 0, 255)
red   = (255, 0, 0)
yellow = (225, 225, 0)
green = (0, 255, 0)

center_top_left = (253, 253)
center_top_right = (347, 253)
center_bottom_left = (253, 347)
center_bottom_right = (347, 347)
center = (300, 300)

out = [[125, 125], [475, 125], [125, 475], [475, 475]]
places = [[0, -40], [-40, 0], [0, 40], [40, 0]]

img_place = 13


class Board:
    running = True

    def __init__(self, size):
        pygame.init()
        self.screen = pygame.display.set_mode(size)
        self.player_color = None
        self.status = "Game in progress.."
        self.dice = 1
        self.turn = 0
        
        # draw board
        self.draw_board()

        # add dice
        dice = pygame.image.load(self.get_dice_png(self.dice))
        self.screen.blit(dice, (600, 520))
        self.dice_rect = pygame.Rect((600, 520), dice.get_size())

        # add players
        self.sprites = pygame.sprite.Group()
        self.player_y = Player(self.sprites, 0)
        self.player_b = Player(self.sprites, 1)
        self.player_g = Player(self.sprites, 2)
        self.player_r = Player(self.sprites, 3)
        self.player_list = [self.player_b, self.player_r, self.player_g, self.player_y]
        self.player = self.player_r

    def main(self):
        while self.running:
            clock.tick(15)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
        
            # add game status label
            for p in self.player_list:
                if p.score == 4:
                    self.status = "{} wins".format(p.get_color_name())
            self.add_label(595, 80, self.status, 20, white)
            
            # add game status label
            self.add_label(595, 160, self.get_turn_label(), 20, white)

            # add score labels
            self.add_label(297, 283, str(self.player_b.score), 20, blue)
            self.add_label(297, 307, str(self.player_g.score), 20, green)
            self.add_label(285, 295, str(self.player_y.score), 20, yellow)
            self.add_label(309, 295, str(self.player_r.score), 20, red)
            
                
            x, y = pygame.mouse.get_pos()
            player = self.get_player_turn()

            # The dice
            if player == "dice" and pygame.mouse.get_pressed()[0] and self.dice_rect.collidepoint(x, y):
                self.roll_dice()
            
            if player != "dice" and self.dice == 6:
                self.player_starts(player)
            if player != "dice":
                self.player_move(player, self.dice)
            if player != "dice" and self.cant_move(player):
                self.change_turn()

            self.sprites.update()
            self.sprites.draw(self.screen)
            pygame.display.flip()
                
            
    def player_starts(self, player):
        x, y = pygame.mouse.get_pos()
        is_out = self.is_point_out(x, y)

        for piece in player.pieces:
            if (pygame.mouse.get_pressed()[0] and
                piece.rect.collidepoint(x, y) and
                is_out):
                
                if piece.pos + 1 in [p.pos for p in player.pieces]:
                    continue

                self.throw_out_piece(player, 1)
               
                self.remove_img(piece.rect, white)
                start_pos = player.get_start_pos()
                piece.rect.x = start_pos[0]
                piece.rect.y = start_pos[1]
                piece.pos += 1
                self.change_turn()

    def player_move(self, player, dice_num):
        x, y = pygame.mouse.get_pos()
        is_out = self.is_point_out(x, y)
        
        for piece in player.pieces:
            if (pygame.mouse.get_pressed()[0] and
                piece.rect.collidepoint(x, y) and
                not is_out):

                if piece.pos + dice_num in [p.pos for p in player.pieces if p.pos != 62]:
                    continue

                if piece.pos + dice_num > 62:
                    continue

                throw = self.throw_out_piece(player, piece.pos + dice_num)
                
                for i in range(dice_num):
                    self.remove_img(piece.rect, self.get_pos_color(piece.rect))
                    self.make_move(player, piece.rect)
                    if i == dice_num - 1 and throw != []:
                        self.remove_img(throw[0][1].rect, self.get_pos_color(throw[0][1].rect))
                        throw[0][1].rect = self.get_free_place(throw[0][0])
                        throw[0][1].pos = 0

                piece.pos += dice_num
                self.change_turn()
                

    def make_move(self, player, rect):
        if self.go_left(rect):
            rect.x -= 32
        elif self.go_right(rect):
            rect.x += 32
        elif self.go_up(rect):
            rect.y -= 32
        elif self.go_down(rect):
            rect.y += 32
        else:
            if ((rect.x > 300 - img_place and player.color == 3) or
                (rect.y > 300 - img_place and player.color != 2)):
                rect.x -= 32 
            elif ((rect.x > 300 - img_place and player.color != 3) or
                  (rect.y < 300 - img_place and player.color == 1)):
                rect.y += 32
            elif ((rect.y < 300 - img_place and player.color != 1) or
                  (rect.x < 300 - img_place and player.color == 0)):
                rect.x += 32
            elif ((rect.x < 300 - img_place and player.color != 0) or
                  (rect.y > 300 - img_place and player.color == 2)):
                rect.y -= 32

        
        self.sprites.draw(self.screen)
        pygame.display.flip()
        pygame.time.delay(400)

    def go_left(self, rect):
        if (rect.y == 332 - img_place and
            rect.x != 364 - img_place and
            rect.x != 76 - img_place):
            return True
        if (rect.y == 364 - img_place and
             (rect.x == 364 - img_place or rect.x == 268 - img_place)):
            return True
        if (rect.x == 332 - img_place and rect.y == 524 - img_place):
            return True
            
        return False
    
    def go_right(self, rect):
        if (rect.y == 268 - img_place and
            rect.x != 524 - img_place and
            rect.x != 236 - img_place):
            return True
        if (rect.y == 236 - img_place and
             (rect.x == 236 - img_place or rect.x == 332 - img_place)):
            return True
        if (rect.x == 268 - img_place and rect.y == 76 - img_place):
            return True
            
        return False
    
    def go_up(self, rect):
        if (rect.x == 268 - img_place and
            rect.y != 364 - img_place and
            rect.y != 76 - img_place):
            return True
        if (rect.x == 236 - img_place and
             (rect.y == 364 - img_place or rect.y == 268 - img_place)):
            return True
        if (rect.y == 332 - img_place and rect.x == 76 - img_place):
            return True
            
        return False
    
    def go_down(self, rect):
        if (rect.x == 332 - img_place and
            rect.y != 524 - img_place and
            rect.y != 236 - img_place):
            return True
        if (rect.x == 364 - img_place and
             (rect.y == 236 - img_place or rect.y == 332 - img_place)):
            return True
        if (rect.y == 268 - img_place and rect.x == 524 - img_place):
            return True
            
        return False

    def throw_out_piece(self, player, pos):
        for i in range(4):
            if player != self.player_list[i]:
                result = self.check_player(self.player_list[i], pos, self.get_diff((player.color, self.player_list[i].color)))
                if result != []:
                    return result
        return []

    def check_player(self, player, pos, diff):
            return [(player, p) for p in player.pieces if p.pos != 0 and pos + diff == p.pos and pos < 57 and p.pos < 57]
            

    def get_diff(self, colors):
        if (colors == (0, 1) or colors == (1, 3) or colors == (3, 2) or colors == (2, 0)):
            return -14
        if (colors == (1, 0) or colors == (3, 1) or colors == (2, 3) or colors == (0, 2)):
            return 14
        if (colors == (3, 0) or colors == (0, 3) or colors == (2, 1) or colors == (1, 2)):
            return -28

    def get_free_place(self, player):
        for i in range(4):
            rect = pygame.Rect(
                (out[player.color][0] + places[i][0] - img_place,
                out[player.color][1] + places[i][1] - img_place),
                player.image.get_size())
            if rect not in [p.rect for p in player.pieces]:
                return rect

    def get_pos_color(self, rect):
        for i in range(4):
            if (rect.x + img_place == start_points[i][0] and
                rect.y + img_place == start_points[i][1]):
                return self.get_color_name(i)
            if (rect.x + img_place == 300 and
                rect.y + img_place > 76 and rect.y + img_place < 300):
                return blue
            if (rect.x + img_place == 300 and
                rect.y + img_place > 300 and rect.y + img_place < 524):
                return green
            if (rect.y + img_place == 300 and
                rect.x + img_place > 76 and rect.x + img_place < 300):
                return yellow
            if (rect.y + img_place == 300 and
                rect.x + img_place > 300 and rect.x + img_place < 524):
                return red
        return white

    def get_color_name(self, num):
        return {
            0: yellow,
            1: blue,
            2: green,
            3: red
            }.get(num, red)

    def remove_img(self, rect, color):
        pygame.draw.circle(self.screen, color, (rect.x + img_place, rect.y + img_place), 15)
        pygame.draw.circle(self.screen, black, (rect.x + img_place, rect.y + img_place), 15, 1)

    def is_point_out(self, x, y):
        for i in range(4):
            if math.sqrt((out[i][0] - x) ** 2 + (out[i][1] - y) ** 2) <= 80:
                return True
        return False

    def roll_dice(self):        
        for i in range(15):
            self.dice = randrange(1, 7)
            dice = pygame.image.load(self.get_dice_png(self.dice))
            self.screen.blit(dice, (600, 520))
            pygame.display.flip()
            pygame.time.delay(20)

        self.change_turn()
        self.sprites.draw(self.screen)
        pygame.display.flip()

    def change_turn(self):
        player = self.get_player_turn()
        
        if player == "dice":
            self.turn = (self.turn + 1) % 8

        if player != "dice" and (self.dice != 6 or self.cant_move(player)): 
            self.turn = (self.turn + 1) % 8
        if player != "dice" and self.dice == 6 and not self.cant_move(player):
            self.turn = (self.turn + 7) % 8

    def cant_move(self, player):
        count = 0
        for piece in player.pieces:
            if ((piece.pos + self.dice > 62) or
                (piece.pos == 0 and self.dice != 6) or
                (piece.pos != 0 and piece.pos + self.dice in [p.pos for p in player.pieces])):
                count += 1
        if count == 4:
            return True
        return False

    def get_player_turn(self):
        if self.turn % 2 == 0:
            return "dice"
        return {
            1: self.player_r,
            3: self.player_g,
            5: self.player_y,
            7: self.player_b
            }.get(self.turn)

    def add_label(self, x, y, label, size, color):
        font = pygame.font.Font(None, size)
        small = False
        if len(label) < 2:
            small = True
        self.delete_last_label(x, y, color, small)
        game_status = font.render(label, 1, black)
        self.screen.blit(game_status, (x, y))


    def get_turn_label(self):
        return {
            0: "Red rolls the dice",
            1: "Red plays",
            2: "Green rolls the dice",
            3: "Green plays",
            4: "Yellow rolls the dice",
            5: "Yellow plays",
            6: "Blue rolls the dice",
            7: "Blue plays"
            }.get(self.turn)
        
    def get_dice_png(self, x):
        return {
            6: '6.png',
            5: '5.png',
            4: '4.png',
            3: '3.png',
            2: '2.png',
            1: '1.png'
            }.get(x, '6.png') 

    def delete_last_label(self, x, y, color, small):
        rect = pygame.Rect(x, y, 130, 20)
        if small:
            rect = pygame.Rect(x, y, 10, 11)
        pygame.draw.rect(self.screen, color, rect)
        
    def draw_triangles(self, color, vertices):
        pygame.draw.polygon(self.screen, color, vertices)
        pygame.draw.polygon(self.screen, black, vertices, 1)
            

    def draw_circles(self, color, begin_x, begin_y, direction_x, direction_y, count_x, count_y, last):
        for i in range(count_y):
            for j in range(count_x):
                if (((count_y > count_x and j == 1 and i < 5) or
                    (count_y < count_x and i == 1 and j < 5)) or
                    (last and i == count_y-1 and j == count_x-1) or
                    (not(last) and ((i == 5 and j == 0) or (i == 0 and j == 5)))):
                    circle_color = color
                else:
                    circle_color = white
                pygame.draw.circle(self.screen, circle_color, (begin_x + direction_x*32*j, begin_y + direction_y*32*i), 15, 0)
                pygame.draw.circle(self.screen, black, (begin_x + direction_x*32*j, begin_y + direction_y*32*i), 15, 1)



    def draw_board(self):
        # white background and sky blue borad
            self.screen.fill(white)
            rect = pygame.Rect(20, 20, 560, 560)
            pygame.draw.rect(self.screen, background, rect)

            #double border line
            pygame.draw.rect(self.screen, black, rect, 3)
            rect = pygame.Rect(14, 14, 571, 571)
            pygame.draw.rect(self.screen, black, rect, 2)
            

            # four houses
            pygame.draw.circle(self.screen, yellow, out[0], 80, 0)
            pygame.draw.circle(self.screen, blue, out[1], 80, 0)
            pygame.draw.circle(self.screen, green, out[2], 80, 0)
            pygame.draw.circle(self.screen, red, out[3], 80, 0)

            # four rooms in each house
            for i in range(4):
                pygame.draw.circle(self.screen, black, out[i], 80, 1)
                for j in range(4):
                    pygame.draw.circle(self.screen, white, (out[i][0] + places[j][0], out[i][1] + places[j][1]), 15, 0)
                    pygame.draw.circle(self.screen, black, (out[i][0] + places[j][0], out[i][1] + places[j][1]), 15, 1)

            # center
            self.draw_triangles(blue, (center_top_left, center_top_right, center))

            
            self.draw_triangles(red, (center_top_right, center_bottom_right, center))
            self.draw_triangles(green, (center_bottom_right, center_bottom_left, center))
            self.draw_triangles(yellow, (center_bottom_left, center_top_left, center))

            # road of circles
            self.draw_circles(blue, 268, 236, 1, -1, 3, 6, True)
            self.draw_circles(red, 364, 268, 1, 1, 6, 3, True)
            self.draw_circles(green, 268, 364, 1, 1, 3, 6, False)
            self.draw_circles(yellow, 236, 268, -1, 1, 6, 3, False)

            for i in range(2):
                for j in range(2):
                    pygame.draw.circle(self.screen, white, (236 + i*128, 236 + j*128), 15, 0)
                    pygame.draw.circle(self.screen, black, (236 + i*128, 236 + j*128), 15, 1)

            # add status label
            font = pygame.font.Font(pygame.font.get_default_font(), 24)
            status_label = font.render("Status:", 1, black)
            self.screen.blit(status_label, (595, 50))

            # add Turn label
            font = pygame.font.Font(pygame.font.get_default_font(), 24)
            status_label = font.render("Turn:", 1, black)
            self.screen.blit(status_label, (595, 130))

            # add another label
            font = pygame.font.Font(pygame.font.get_default_font(), 12)
            label = font.render("The dice...", 1, black)
            self.screen.blit(label, (595, 500))


if __name__ == '__main__':
    Board((725, 600)).main()
