import pygame
import time
from random import *
from player import *
from board import *


clock = pygame.time.Clock()


class Main:
    running = True

    def __init__(self, size):
        """Adds status lable, the dice and the players"""
        pygame.init()
        self.screen = pygame.display.set_mode(size)
        self.dice = 1
        self.roll_dice_count = 2

        self.board = Board(self.screen)

        """Add dice"""
        dice = pygame.image.load(self.get_dice_png(self.dice))
        self.screen.blit(dice, (600, 520))
        self.dice_rect = pygame.Rect((600, 520), dice.get_size())

        self.sprites = pygame.sprite.Group()
        self.player_y = Player(self.sprites, 0)
        self.player_b = Player(self.sprites, 1)
        self.player_g = Player(self.sprites, 2)
        self.player_r = Player(self.sprites, 3)
        self.player_list = [self.player_b, self.player_r,
                            self.player_g, self.player_y]

        rand_player = randrange(1, 7)
        if rand_player % 2 == 0:
            rand_player += 1
        self.player = self.get_player_turn(rand_player)

        self.board.add_label(595, 130, self.player.get_color_name(),
                             20, self.board.WHITE)
        self.turn = rand_player - 1

    def main(self):
        while self.running:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            """Check if any player won the game and change status."""
            for p in self.player_list:
                if p.score == 4:
                    self.status = "{} wins".format(p.get_color_name())
                    self.board.add_label(595, 70, self.status,
                                         20, self.board.WHITE)
                    return

            """Add game turn label"""
            self.board.add_label(595, 190, self.get_turn_label(),
                                 20, self.board.WHITE)

            """Add score label"""
            self.board.add_label(297, 283, str(self.player_b.score),
                                 20, self.board.BLUE)
            self.board.add_label(297, 307, str(self.player_g.score),
                                 20, self.board.GREEN)
            self.board.add_label(285, 295, str(self.player_y.score),
                                 20, self.board.YELLOW)
            self.board.add_label(309, 295, str(self.player_r.score),
                                 20, self.board.RED)

            x, y = pygame.mouse.get_pos()
            player = self.get_player_turn(self.turn)

            """Roll the dice"""
            next_player = self.get_player_turn(self.turn + 1)
            if (player == "dice" and self.player == next_player
               and pygame.mouse.get_pressed()[0] and
               self.dice_rect.collidepoint(x, y)):
                self.roll_dice()
            elif player == "dice" and self.player != next_player:
                self.roll_dice()

            """Players play"""
            if player == self.player and self.dice == 6:
                self.player_starts(player)
            if player == self.player:
                self.player_move(player)
            if player != "dice" and self.cant_move_count(player) == 4:
                pygame.time.delay(1000)
                self.change_turn()
            if (player != self.player and player != "dice" and
               self.cant_move_count(player) != 4):
                self.play(player)

            self.sprites.update()
            self.sprites.draw(self.screen)
            pygame.display.flip()

    def player_starts(self, player):
        """Moves player's piece from out zone to start position"""
        x, y = pygame.mouse.get_pos()
        is_out = self.is_point_out(x, y)

        for piece in player.pieces:
            if (pygame.mouse.get_pressed()[0] and
               piece.rect.collidepoint(x, y) and
               is_out
               and self.can_move(player, piece)):
                self.piece_starts(player, piece)

    def piece_starts(self, player, piece):
        """Move piece to start position"""
        throw = self.throw_out_piece(player,
                                     self.get_next_board_pos(piece,
                                                             player.color))

        if throw != []:
            self.remove_img(throw[0][1].rect,
                            self.board.get_pos_color(throw[0][1].rect))
            throw[0][1].rect = self.get_free_place(throw[0][0])
            throw[0][1].pos = 0

            self.sprites.update()
            self.sprites.draw(self.screen)
            pygame.display.flip()

        self.remove_img(piece.rect, self.board.WHITE)
        start_pos = player.get_start_pos()
        piece.rect.x = start_pos[0]
        piece.rect.y = start_pos[1]
        piece.pos += 1
        self.change_turn()

    def player_move(self, player):
        """Moves player's piece with the number on dice positions"""
        x, y = pygame.mouse.get_pos()
        is_out = self.is_point_out(x, y)

        for piece in player.pieces:
            if (pygame.mouse.get_pressed()[0] and
               piece.rect.collidepoint(x, y) and
               not is_out and
               self.can_move(player, piece)):
                self.move_piece(player, piece)

    def move_piece(self, player, piece):
        """Move piece with the number on the dice positions"""
        throw = self.throw_out_piece(player,
                                     self.get_next_board_pos(piece,
                                                             player.color))

        for i in range(self.dice):
            if i == self.dice - 1 and throw != []:
                self.remove_img(throw[0][1].rect,
                                self.board.get_pos_color(throw[0][1].rect))
                throw[0][1].rect = self.get_free_place(throw[0][0])
                throw[0][1].pos = 0

                self.sprites.update()
                self.sprites.draw(self.screen)
                pygame.display.flip()

            self.remove_img(piece.rect, self.board.get_pos_color(piece.rect))
            self.make_move(player, piece.rect)

        piece.pos += self.dice
        self.change_turn()

    def throw_out_piece(self, player, pos):
        """Checks if the piece can throw out piece from other player,
        if it can it returns list ot tupel of the player and the piece"""
        for other_player in self.player_list:
            if other_player != player:
                result = [(other_player, p) for p in
                          other_player.pieces if pos == p.board_pos]
                if result != []:
                    return result
        return []

    def play(self, player):
        """Controls the moving of the pieces if the player is a computer"""
        pygame.time.delay(1000)
        if self.cant_move_count(player) == 4:
            self.change_turn()
            return
        self.decide_move(player)
        pygame.time.delay(500)

    def decide_move(self, player):
        """Desides what piece to move"""
        count = self.cant_move_count(player)
        if count == 3:
            for piece in player.pieces:
                if self.can_move(player, piece):
                    self.move(player, piece)
                    return

        for piece in player.pieces:
            throw = self.throw_out_piece(player,
                                         self.get_next_board_pos(piece,
                                                                 player.color))
            if throw != []:
                self.move(player, piece)
                return

        self.change_closest(player)
        front_list = [p.close_in_front for p in player.pieces
                      if p.close_in_front != 0]
        back_list = [p.close_behind for p in player.pieces
                     if p.close_behind != 0]
        min_front = 56
        min_behind = 56

        for piece in player.pieces:
            if not self.can_move(player, piece):
                if piece.close_in_front != 0:
                    front_list.remove(piece.close_in_front)
                if piece.close_behind != 0:
                    back_list.remove(piece.close_behind)
                continue

            start_pos = self.get_board_start_pos(player.color)
            start_positions = [1, 15, 29, 43]
            start_positions.remove(start_pos)
            if piece.board_pos in start_positions:
                self.move(player, piece)
                return

            if front_list != [] and min_front > min(front_list):
                min_front = min(front_list)
            if back_list != [] and min_behind > min(back_list):
                min_behind = min(back_list)

            if min_behind < self.dice:
                if piece.close_in_front != 0:
                    front_list.remove(piece.close_in_front)
                if piece.close_behind != 0:
                    back_list.remove(piece.close_behind)
                continue

            if (min_front > min_behind and
               piece.close_behind == min_behind):
                self.move(player, piece)
                return
            if (min_front < min_behind and
               piece.close_in_front == min_front):
                self.move(player, piece)
                return

        for piece in player.pieces:
            if self.can_move(player, piece):
                self.move(player, piece)
                return

    def change_closest(self, player):
        """Counts the closest back and front pieces for every piece
        of this player"""
        for piece in player.pieces:
            piece.close_in_front = 0
            piece.close_behind = 0
            min_in_front = 56
            min_behind = 56
            for other_player in self.player_list:
                if other_player != player:
                    min_dist = self.min_front_dist(player, piece, other_player)
                    if min_in_front > min_dist:
                        min_in_front = min_dist
                    min_dist = self.min_behind_dist(player, piece,
                                                    other_player)
                    if min_behind > min_dist:
                        min_behind = min_dist
            if min_in_front != 56:
                piece.close_in_front = min_in_front
            if min_behind != 56:
                piece.close_behind = min_behind

    def min_front_dist(self, player, piece, other_player):
        """Counts the closest piece of the other players in front"""
        min_dist = 56
        if not self.can_move(player, piece):
            return min_dist

        next_pos = piece.board_pos + self.dice
        if piece.pos == 0:
            next_pos = self.get_board_start_pos(player.color)

        if next_pos > 56:
            next_pos -= 56

        for p in other_player.pieces:
            pos = p.board_pos
            if pos != 0 and pos < next_pos:
                pos += 56
            if pos != 0 and pos - next_pos < min_dist:
                min_dist = pos - next_pos
        return min_dist

    def min_behind_dist(self, player, piece, other_player):
        """Counts the closest piece of the other players from behind"""
        min_dist = 56
        if not self.can_move(player, piece):
            return min_dist

        next_pos = piece.board_pos + self.dice
        if piece.pos == 0:
            next_pos = self.get_board_start_pos(player.color)

        if next_pos > 56:
            next_pos -= 56

        for p in other_player.pieces:
            if p.board_pos != 0 and p.board_pos > next_pos:
                next_pos += 56
            if p.board_pos != 0 and next_pos - p.board_pos < min_dist:
                min_dist = next_pos - p.board_pos
        return min_dist

    def move(self, player, piece):
        if piece.pos == 0 and self.dice == 6:
            self.piece_starts(player, piece)
        else:
            self.move_piece(player, piece)

    def make_move(self, player, rect):
        """Moves the piece in the corect direction"""
        if self.board.go_left(rect):
            rect.x -= 32
        elif self.board.go_right(rect):
            rect.x += 32
        elif self.board.go_up(rect):
            rect.y -= 32
        elif self.board.go_down(rect):
            rect.y += 32
        else:
            if ((rect.x > 300 - self.board.IMG_PLACE and player.color == 3) or
               (rect.y > 300 - self.board.IMG_PLACE and player.color != 2)):
                rect.x -= 32
            elif ((rect.x > 300 - self.board.IMG_PLACE and player.color != 3)
                  or (rect.y < 300 - self.board.IMG_PLACE and
                      player.color == 1)):
                rect.y += 32
            elif ((rect.y < 300 - self.board.IMG_PLACE and player.color != 1)
                  or (rect.x < 300 - self.board.IMG_PLACE and
                      player.color == 0)):
                rect.x += 32
            elif ((rect.x < 300 - self.board.IMG_PLACE and player.color != 0)
                  or (rect.y > 300 - self.board.IMG_PLACE and
                      player.color == 2)):
                rect.y -= 32

        self.sprites.draw(self.screen)
        pygame.display.flip()
        pygame.time.delay(400)

    def get_free_place(self, player):
        """Returns one free place of the player's out teritory"""
        for i in range(4):
            rect = pygame.Rect(
                (self.board.OUT[player.color][0] + self.board.PLACES[i][0] -
                 self.board.IMG_PLACE, self.board.OUT[player.color][1] +
                 self.board.PLACES[i][1] - self.board.IMG_PLACE),
                player.image.get_size())
            if rect not in [p.rect for p in player.pieces]:
                return rect

    def get_next_board_pos(self, piece, color):
        """Returns the number of the board position of the pice
        if it moves with the number on dice positions"""
        if piece.board_pos == 0 and self.dice == 6:
            return {
                0: 29,
                1: 43,
                2: 15,
                3: 1}.get(color)

        pos = piece.board_pos + self.dice
        if pos > 56:
            pos -= 56
        return pos

    def get_board_start_pos(self, color):
        return {
            0: 29,
            1: 43,
            2: 15,
            3: 1}.get(color)

    def on_board(self, piece):
        if piece.pos == 0 or piece.pos > 56:
            return False
        return True

    def remove_img(self, rect, color):
        pygame.draw.circle(self.screen, color,
                           (rect.x + self.board.IMG_PLACE,
                            rect.y + self.board.IMG_PLACE), 15)
        pygame.draw.circle(self.screen, self.board.BLACK,
                           (rect.x + self.board.IMG_PLACE,
                            rect.y + self.board.IMG_PLACE), 15, 1)

    def is_point_out(self, x, y):
        for i in range(4):
            if math.sqrt((self.board.OUT[i][0] - x) ** 2 +
                         (self.board.OUT[i][1] - y) ** 2) <= 80:
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
        player = self.get_player_turn(self.turn)

        if player == "dice":
            self.turn += 1

        if player != "dice" and self.dice != 6 and player.all_out:
            if self.roll_dice_count > 0:
                self.turn = (self.turn + 7) % 8
                self.roll_dice_count -= 1
                return

        if player != "dice" and (self.dice != 6 or
                                 self.cant_move_count(player) == 4):
            next_player = self.get_player_turn((self.turn + 2) % 8)
            if next_player.all_out:
                self.roll_dice_count = 2
            self.turn = (self.turn + 1) % 8

        if (player != "dice" and self.dice == 6 and
           self.cant_move_count(player) != 4):
            self.turn = (self.turn + 7) % 8

    def cant_move_count(self, player):
        """Counts player's pieces that can't move"""
        count = 0
        for piece in player.pieces:
            if not self.can_move(player, piece):
                count += 1
        return count

    def can_move(self, player, piece):
        """Checks if a piece can move"""
        if ((piece.pos + self.dice > 62) or
            (piece.pos == 0 and self.dice != 6) or
            (piece.pos != 0 and piece.pos + self.dice in
             [p.pos for p in player.pieces if p.pos != 62]) or
            (piece.pos == 0 and self.dice == 6 and 1 in
             [p.pos for p in player.pieces])):
            return False
        return True

    def get_player_turn(self, turn):
        if turn % 2 == 0:
            return "dice"
        return {
            1: self.player_r,
            3: self.player_g,
            5: self.player_y,
            7: self.player_b}.get(turn)

    def get_turn_label(self):
        return {
            0: "Red rolls the dice",
            1: "Red plays",
            2: "Green rolls the dice",
            3: "Green plays",
            4: "Yellow rolls the dice",
            5: "Yellow plays",
            6: "Blue rolls the dice",
            7: "Blue plays"}.get(self.turn)

    def get_dice_png(self, x):
        return {
            6: '6.png',
            5: '5.png',
            4: '4.png',
            3: '3.png',
            2: '2.png',
            1: '1.png'}.get(x, '6.png')

if __name__ == '__main__':
    Main((725, 600)).main()
