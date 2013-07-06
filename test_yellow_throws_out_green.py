import unittest

from main import *


class YellowThrowsOutGreenTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        self.game = Main((725, 600))
        self.game.dice = 6

    def test_yellow_throws_out_green(self):
        self.game.play(self.game.player_y)
        pieces = [p for p in self.game.player_y.pieces if p.pos != 0]
        self.assertTrue(pieces != [])
        self.y_piece1 = pieces[0]
        self.assertEqual(self.y_piece1.pos, 1)

        self.game.player_y.update()
        self.assertEqual(self.y_piece1.board_pos, 29)

        self.game.dice = 5
        self.game.play(self.game.player_y)
        self.assertEqual(self.y_piece1.pos, 6)

        self.game.player_y.update()
        self.assertEqual(self.y_piece1.board_pos, 34)

        self.game.dice = 6
        for i in range(3):
            self.game.play(self.game.player_g)
            pieces = [p for p in self.game.player_g.pieces if p.pos != 0]
            self.g_piece = pieces[0]
            self.assertEqual(self.g_piece.pos, 1 + i*6)

            self.game.player_g.update()
            self.assertEqual(self.g_piece.board_pos, 15 + i*6)

        self.game.dice = 2
        self.game.play(self.game.player_g)
        self.assertEqual(self.g_piece.pos, 15)

        self.game.player_g.update()
        self.assertEqual(self.g_piece.board_pos, 29)

        self.game.dice = 6
        self.game.play(self.game.player_y)
        pieces = [p for p in self.game.player_y.pieces if p.pos != 0 and
                  p != self.y_piece1]
        self.assertTrue(pieces != [])
        self.y_piece2 = pieces[0]
        self.assertEqual(self.y_piece2.pos, 1)
        self.assertEqual(self.g_piece.pos, 0)

        self.game.player_g.update()
        self.game.player_y.update()
        self.assertEqual(self.g_piece.board_pos, 0)
        self.assertEqual(self.y_piece2.board_pos, 29)


if __name__ == '__main__':
    unittest.main()
