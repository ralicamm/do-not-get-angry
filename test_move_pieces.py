import unittest

from main import *


class MovePiecesTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        self.game = Main((725, 600))
        self.game.dice = 6

        y_pieces = [p for p in self.game.player_y.pieces]
        self.y_piece = y_pieces.pop()

        b_pieces = [p for p in self.game.player_b.pieces]
        self.b_piece = b_pieces.pop()

        g_pieces = [p for p in self.game.player_g.pieces]
        self.g_piece = g_pieces.pop()

        r_pieces = [p for p in self.game.player_r.pieces]
        self.r_piece = r_pieces.pop()

    def test_yellow_piece_starts(self):
        self.game.piece_starts(self.game.player_y, self.y_piece)
        self.assertEqual(self.y_piece.pos, 1)

        self.game.player_y.update()
        self.assertEqual(self.y_piece.board_pos, 29)

    def test_blue_piece_starts(self):
        self.game.piece_starts(self.game.player_b, self.b_piece)
        self.assertEqual(self.b_piece.pos, 1)

        self.game.player_b.update()
        self.assertEqual(self.b_piece.board_pos, 43)

    def test_green_piece_starts(self):
        self.game.piece_starts(self.game.player_g, self.g_piece)
        self.assertEqual(self.g_piece.pos, 1)

        self.game.player_g.update()
        self.assertEqual(self.g_piece.board_pos, 15)

    def test_red_piece_starts(self):
        self.game.piece_starts(self.game.player_r, self.r_piece)
        self.assertEqual(self.r_piece.pos, 1)

        self.game.player_r.update()
        self.assertEqual(self.r_piece.board_pos, 1)

    def test_yellow_move_piece(self):
        self.game.piece_starts(self.game.player_y, self.y_piece)
        self.game.dice = 5
        self.game.move_piece(self.game.player_y, self.y_piece)
        self.assertEqual(self.y_piece.pos, 6)

        self.game.player_y.update()
        self.assertEqual(self.y_piece.board_pos, 34)

    def test_blue_move_piece(self):
        self.game.piece_starts(self.game.player_b, self.b_piece)
        self.game.dice = 4
        self.game.move_piece(self.game.player_b, self.b_piece)
        self.assertEqual(self.b_piece.pos, 5)

        self.game.player_b.update()
        self.assertEqual(self.b_piece.board_pos, 47)

    def test_green_move_piece(self):
        self.game.piece_starts(self.game.player_g, self.g_piece)
        self.game.dice = 3
        self.game.move_piece(self.game.player_g, self.g_piece)
        self.assertEqual(self.g_piece.pos, 4)

        self.game.player_g.update()
        self.assertEqual(self.g_piece.board_pos, 18)

    def test_red_move_piece(self):
        self.game.piece_starts(self.game.player_r, self.r_piece)
        self.game.dice = 2
        self.game.move_piece(self.game.player_r, self.r_piece)
        self.assertEqual(self.r_piece.pos, 3)

        self.game.player_r.update()
        self.assertEqual(self.r_piece.board_pos, 3)

if __name__ == '__main__':
    unittest.main()
