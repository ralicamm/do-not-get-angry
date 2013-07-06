import unittest

from main import *


class RedThrowsOutGreenTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        self.game = Main((725, 600))
        self.game.dice = 6

        g_pieces = [p for p in self.game.player_g.pieces]
        self.g_piece = g_pieces.pop()

        r_pieces = [p for p in self.game.player_r.pieces]
        self.r_piece = r_pieces.pop()

    def test_red_throws_out_green(self):
        self.game.piece_starts(self.game.player_g, self.g_piece)
        self.game.dice = 4
        self.game.move_piece(self.game.player_g, self.g_piece)
        self.assertEqual(self.g_piece.pos, 5)

        self.game.player_g.update()
        self.assertEqual(self.g_piece.board_pos, 19)

        self.game.dice = 6
        self.game.piece_starts(self.game.player_r, self.r_piece)

        for i in range(3):
            self.game.move_piece(self.game.player_r, self.r_piece)
            self.assertEqual(self.r_piece.pos, 7 + i*6)

            self.game.player_r.update()
            self.assertEqual(self.r_piece.board_pos, 7 + i*6)

        self.game.player_g.update()
        self.assertEqual(self.g_piece.board_pos, 0)

if __name__ == '__main__':
    unittest.main()
