import unittest

from main import *


class BlueWinsTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        self.game = Main((725, 600))

    def test_blue_wins(self):
        for piece in self.game.player_b.pieces:
            self.game.dice = 6
            self.game.piece_starts(self.game.player_b, piece)

            self.game.dice = 61
            self.game.move_piece(self.game.player_b, piece)
            self.assertEqual(piece.pos, 62)

            self.game.player_b.update()
            self.assertEqual(piece.board_pos, 0)

        self.game.check_winner()
        self.assertEqual(self.game.status, "Blue wins!")

if __name__ == '__main__':
    unittest.main()
