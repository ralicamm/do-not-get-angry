import unittest

from main import *


class BlueThrowsOutYellowTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        self.game = Main((725, 600))
        self.game.dice = 6

        y_pieces = [p for p in self.game.player_y.pieces]
        self.y_piece = y_pieces.pop()

        b_pieces = [p for p in self.game.player_b.pieces]
        self.b_piece = b_pieces.pop()

    def test_blue_throws_out_yellow(self):
        self.game.piece_starts(self.game.player_b, self.b_piece)
        self.game.dice = 11
        self.game.move_piece(self.game.player_b, self.b_piece)
        self.assertEqual(self.b_piece.pos, 12)

        self.game.player_b.update()
        self.assertEqual(self.b_piece.board_pos, 54)

        self.game.piece_starts(self.game.player_y, self.y_piece)
        self.game.dice = 30
        self.game.move_piece(self.game.player_y, self.y_piece)
        self.assertEqual(self.y_piece.pos, 31)

        self.game.player_y.update()
        self.assertEqual(self.y_piece.board_pos, 3)

        self.game.dice = 5
        self.game.move_piece(self.game.player_b, self.b_piece)
        self.assertEqual(self.b_piece.pos, 17)

        self.game.player_b.update()
        self.assertEqual(self.b_piece.board_pos, 3)

        self.game.player_y.update()
        self.assertEqual(self.y_piece.pos, 0)
        self.assertEqual(self.y_piece.board_pos, 0)

if __name__ == '__main__':
    unittest.main()
