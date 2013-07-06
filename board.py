import pygame


class Board:
    BACKGROUND = (164, 211, 238)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)
    YELLOW = (225, 225, 0)
    GREEN = (0, 255, 0)

    TOP_LEFT = (253, 253)
    TOP_RIGHT = (347, 253)
    BOTTOM_LEFT = (253, 347)
    BOTTOM_RIGHT = (347, 347)
    CENTER = (300, 300)

    START_POINTS = [(76, 268), (332, 76), (268, 524), (524, 332)]
    OUT = [[125, 125], [475, 125], [125, 475], [475, 475]]
    PLACES = [[0, -40], [-40, 0], [0, 40], [40, 0]]

    IMG_PLACE = 13

    def __init__(self, screen):
        self.screen = screen

        self.draw_board()

    def add_label(self, x, y, label, size, color):
        font = pygame.font.Font(None, size)
        small = False
        if len(label) < 2:
            small = True
        self.delete_last_label(x, y, color, small)
        game_status = font.render(label, 1, self.BLACK)
        self.screen.blit(game_status, (x, y))

    def delete_last_label(self, x, y, color, small):
        rect = pygame.Rect(x, y, 130, 20)
        if small:
            rect = pygame.Rect(x, y, 10, 11)
        pygame.draw.rect(self.screen, color, rect)

    def get_pos_color(self, rect):
        """Returns the color of the position"""
        for i in range(4):
            if (rect.x + self.IMG_PLACE == self.START_POINTS[i][0] and
               rect.y + self.IMG_PLACE == self.START_POINTS[i][1]):
                return self.get_color_name(i)
            if (rect.x + self.IMG_PLACE == 300 and
               rect.y + self.IMG_PLACE > 76 and
               rect.y + self.IMG_PLACE < 300):
                return self.BLUE
            if (rect.x + self.IMG_PLACE == 300 and
               rect.y + self.IMG_PLACE > 300 and
               rect.y + self.IMG_PLACE < 524):
                return self.GREEN
            if (rect.y + self.IMG_PLACE == 300 and
               rect.x + self.IMG_PLACE > 76 and
               rect.x + self.IMG_PLACE < 300):
                return self.YELLOW
            if (rect.y + self.IMG_PLACE == 300 and
               rect.x + self.IMG_PLACE > 300 and
               rect.x + self.IMG_PLACE < 524):
                return self.RED
        return self.WHITE

    def get_color_name(self, num):
        return {
            0: self.YELLOW,
            1: self.BLUE,
            2: self.GREEN,
            3: self.RED}.get(num, self.RED)

    def go_left(self, rect):
        """Checks if the piece have to go left"""
        if (rect.y == 332 - self.IMG_PLACE and
           rect.x != 364 - self.IMG_PLACE and
           rect.x != 76 - self.IMG_PLACE):
            return True
        if (rect.y == 364 - self.IMG_PLACE and
           (rect.x == 364 - self.IMG_PLACE or rect.x == 268 - self.IMG_PLACE)):
            return True
        if (rect.x == 332 - self.IMG_PLACE and rect.y == 524 - self.IMG_PLACE):
            return True

        return False

    def go_right(self, rect):
        """Checks if the piece have to go right"""
        if (rect.y == 268 - self.IMG_PLACE and
           rect.x != 524 - self.IMG_PLACE and
           rect.x != 236 - self.IMG_PLACE):
            return True
        if (rect.y == 236 - self.IMG_PLACE and
           (rect.x == 236 - self.IMG_PLACE or rect.x == 332 - self.IMG_PLACE)):
            return True
        if (rect.x == 268 - self.IMG_PLACE and rect.y == 76 - self.IMG_PLACE):
            return True

        return False

    def go_up(self, rect):
        """Checks if the piece have to go up"""
        if (rect.x == 268 - self.IMG_PLACE and
           rect.y != 364 - self.IMG_PLACE and
           rect.y != 76 - self.IMG_PLACE):
            return True
        if (rect.x == 236 - self.IMG_PLACE and
           (rect.y == 364 - self.IMG_PLACE or rect.y == 268 - self.IMG_PLACE)):
            return True
        if (rect.y == 332 - self.IMG_PLACE and rect.x == 76 - self.IMG_PLACE):
            return True

        return False

    def go_down(self, rect):
        """Checks if the piece have to go down"""
        if (rect.x == 332 - self.IMG_PLACE and
           rect.y != 524 - self.IMG_PLACE and
           rect.y != 236 - self.IMG_PLACE):
            return True
        if (rect.x == 364 - self.IMG_PLACE and
           (rect.y == 236 - self.IMG_PLACE or rect.y == 332 - self.IMG_PLACE)):
            return True
        if (rect.y == 268 - self.IMG_PLACE and rect.x == 524 - self.IMG_PLACE):
            return True

        return False

    def draw_board(self):
        """Draws the board and adds the main labels"""
        self.screen.fill(self.WHITE)
        rect = pygame.Rect(20, 20, 560, 560)
        pygame.draw.rect(self.screen, self.BACKGROUND, rect)

        pygame.draw.rect(self.screen, self.BLACK, rect, 3)
        rect = pygame.Rect(14, 14, 571, 571)
        pygame.draw.rect(self.screen, self.BLACK, rect, 2)

        pygame.draw.circle(self.screen, self.YELLOW, self.OUT[0], 80, 0)
        pygame.draw.circle(self.screen, self.BLUE, self.OUT[1], 80, 0)
        pygame.draw.circle(self.screen, self.GREEN, self.OUT[2], 80, 0)
        pygame.draw.circle(self.screen, self.RED, self.OUT[3], 80, 0)

        for i in range(4):
            pygame.draw.circle(self.screen, self.BLACK, self.OUT[i], 80, 1)
            for j in range(4):
                pygame.draw.circle(
                    self.screen, self.WHITE,
                    (self.OUT[i][0] + self.PLACES[j][0],
                     self.OUT[i][1] + self.PLACES[j][1]),
                    15, 0)
                pygame.draw.circle(
                    self.screen, self.BLACK,
                    (self.OUT[i][0] + self.PLACES[j][0],
                     self.OUT[i][1] + self.PLACES[j][1]),
                    15, 1)

        self.draw_triangles(self.BLUE, (self.TOP_LEFT, self.TOP_RIGHT,
                                        self.CENTER))
        self.draw_triangles(self.RED, (self.TOP_RIGHT, self.BOTTOM_RIGHT,
                                       self.CENTER))
        self.draw_triangles(self.GREEN, (self.BOTTOM_RIGHT, self.BOTTOM_LEFT,
                                         self.CENTER))
        self.draw_triangles(self.YELLOW, (self.BOTTOM_LEFT, self.TOP_LEFT,
                                          self.CENTER))

        self.draw_circles(self.BLUE, 268, 236, 1, -1, 3, 6, True)
        self.draw_circles(self.RED, 364, 268, 1, 1, 6, 3, True)
        self.draw_circles(self.GREEN, 268, 364, 1, 1, 3, 6, False)
        self.draw_circles(self.YELLOW, 236, 268, -1, 1, 6, 3, False)

        for i in range(2):
            for j in range(2):
                pygame.draw.circle(self.screen, self.WHITE,
                                   (236 + i*128, 236 + j*128), 15, 0)
                pygame.draw.circle(self.screen, self.BLACK,
                                   (236 + i*128, 236 + j*128), 15, 1)

        self.add_label(595, 50, "Status:", 24, self.WHITE)
        self.add_label(595, 110, "You play with:", 24, self.WHITE)
        self.add_label(595, 170, "Turn:", 24, self.WHITE)
        self.add_label(595, 500, "The dice...", 20, self.WHITE)

    def draw_triangles(self, color, vertices):
        pygame.draw.polygon(self.screen, color, vertices)
        pygame.draw.polygon(self.screen, self.BLACK, vertices, 1)

    def draw_circles(self, color, begin_x, begin_y,
                     direction_x, direction_y, count_x, count_y, last):
        for i in range(count_y):
            for j in range(count_x):
                if (((count_y > count_x and j == 1 and i < 5) or
                    (count_y < count_x and i == 1 and j < 5)) or
                    (last and i == count_y - 1 and j == count_x - 1) or
                    (not(last) and ((i == 5 and j == 0) or
                                   (i == 0 and j == 5)))):
                    circle_color = color
                else:
                    circle_color = self.WHITE
                pygame.draw.circle(self.screen, circle_color,
                                   (begin_x + direction_x*32*j,
                                    begin_y + direction_y*32*i), 15, 0)
                pygame.draw.circle(self.screen, self.BLACK,
                                   (begin_x + direction_x*32*j,
                                    begin_y + direction_y*32*i), 15, 1)
