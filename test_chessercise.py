#!/usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = 'Rohit Choramle'


"""
This module implements unit test cases for `chessercise.py` module.
"""


import unittest
from chessercise import linear_traverse, diagonal_traverse, compound_traverse, get_pos


class LinearTraverseTestCase(unittest.TestCase):

    def setUp(self):
        self.positions = [
            ('d5', 'TOP', 9, False, ['d6', 'd7', 'd8']),
            ('a8', 'LEFT', 1, False, []),
            ('h8', 'RIGHT', 1, False, []),
            ('f8', 'RIGHT', 3, True, []),
            ]

    def test_linear_traverse_courses(self):
        for pos in self.positions:
            output = linear_traverse(pos[0][0], int(pos[0][1]), pos[1], pos[2], pos[3])
            self.assertEqual(output, pos[4])


class DiagonalTraverseTestCase(unittest.TestCase):

    def setUp(self):
        self.positions = [
            ('d5', 'RTOP', 9, False, ['e6', 'f7', 'g8']),
            ('a8', 'LTOP', 1, False, []),
            ('h8', 'RBOTTOM', 1, False, []),
            ('h8', 'LBOTTOM', 1, False, ['g7']),
            ('f8', 'LBOTTOM', 3, True, ['e7', 'd6', 'c5']),
            ]

    def test_diagonal_traverse_courses(self):
        for pos in self.positions:
            output = diagonal_traverse(pos[0][0], int(pos[0][1]), pos[1], pos[2], pos[3])
            self.assertEqual(output, pos[4])


class CompoundTraverseTestCase(unittest.TestCase):

    def setUp(self):
        self.positions = [
            ('d5', [('TOP', 1), ('BOTTOM', 1)], False, ['d6', 'd5']),
            ('a8', [('LTOP', 1), ()], False, []),
            ('h8', [('LBOTTOM', 2), ()], False, ['g7', 'f6']),
            ('h8', [('LBOTTOM', 2), ('RIGHT', 3)], True, []),
            ('d2', [('RTOP', 1), ('TOP', 1)], True, ['e3', 'e4']),
            ('d2', [('BOTTOM', 3), ('LTOP', 3)], False, ['d1', 'c2', 'b3', 'a4']),
            ('d2', [('BOTTOM', 3), ('LTOP', 3)], True, []),
            ]

    def test_compound_traverse_courses(self):
        for pos in self.positions:
            output = compound_traverse(pos[0][0], int(pos[0][1]), pos[1], pos[2])
            self.assertEqual(output, pos[3])


class GetPosTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_get_pawn_pos(self):
        self.assertEqual(get_pos('PAWN', 'g5'), set(['g6', 'f6', 'h6']))
        self.assertEqual(get_pos('PAWN', 'a8'), set([]))
        self.assertEqual(get_pos('PAWN', 'h8'), set([]))
        self.assertEqual(get_pos('PAWN', 'a4'), set(['a5', 'b5']))
        self.assertEqual(get_pos('PAWN', 'h3'), set(['g4', 'h4']))

    def test_get_rook_pos(self):
        self.assertEqual(get_pos('ROOK', 'g5'), set(['g6', 'g2', 'g8', 'e5', 'a5', 'c5', 'h5', 'g3', 'g4', 'd5', 'g7', 'g1', 'b5', 'f5']))
        self.assertEqual(get_pos('ROOK', 'd2'), set(['f2', 'g2', 'b2', 'h2', 'a2', 'd8', 'c2', 'd6', 'd7', 'd4', 'd5', 'd3', 'e2', 'd1']))
        self.assertEqual(get_pos('ROOK', 'g1'), set(['g7', 'g6', 'g5', 'g4', 'g3', 'g2', 'f1', 'h1', 'g8', 'a1', 'b1', 'c1', 'e1', 'd1']))
        self.assertEqual(get_pos('ROOK', 'h1'), set(['f1', 'h8', 'g1', 'h2', 'h3', 'h6', 'h7', 'h4', 'h5', 'a1', 'b1', 'c1', 'e1', 'd1']))
        self.assertEqual(get_pos('ROOK', 'f8'), set(['f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'h8', 'g8', 'c8', 'e8', 'd8', 'a8', 'b8']))

    def test_get_bishop_pos(self):
        self.assertEqual(get_pos('BISHOP','g5'), set(['f4', 'f6', 'h6', 'h4', 'd8', 'e7', 'd2', 'c1', 'e3']))
        self.assertEqual(get_pos('BISHOP','d2'), set(['g5', 'f4', 'h6', 'b4', 'a5', 'c3', 'c1', 'e1', 'e3']))
        self.assertEqual(get_pos('BISHOP','g1'), set(['f2', 'h2', 'b6', 'e3', 'a7', 'd4', 'c5']))
        self.assertEqual(get_pos('BISHOP','h1'), set(['f3', 'g2', 'b7', 'a8', 'e4', 'd5', 'c6']))
        self.assertEqual(get_pos('BISHOP','f8'), set(['g7', 'h6', 'b4', 'a3', 'd6', 'e7', 'c5']))

    def test_get_queen_pos(self):
        self.assertEqual(get_pos('QUEEN','g5'), set(['f4', 'f5', 'f6', 'h6', 'h4', 'h5', 'b5', 'd8', 'd5', 'd2', 'c1',
                                                      'c5', 'g7', 'g6', 'g4', 'g3', 'g2', 'g1', 'g8', 'a5', 'e5', 'e7', 'e3']))
        self.assertEqual(get_pos('QUEEN','d2'), set(['f2', 'f4', 'd8', 'h2', 'h6', 'b4', 'b2', 'd6', 'd7', 'd4', 'd5',
                                                     'd3', 'd1', 'g5', 'g2', 'a2', 'a5', 'c3', 'c2', 'c1', 'e1', 'e3', 'e2']))
        self.assertEqual(get_pos('QUEEN','g1'), set(['g7', 'g6', 'g5', 'g4', 'g3', 'g2', 'f1', 'h2', 'h1', 'f2', 'g8',
                                                     'a1', 'b6', 'c5', 'b1', 'a7', 'c1', 'e1', 'd4', 'e3', 'd1']))
        self.assertEqual(get_pos('QUEEN','h1'), set(['f1', 'h8', 'f3', 'g2', 'g1', 'h2', 'h3', 'h6', 'h7', 'h4', 'h5',
                                                     'a1', 'b7', 'b1', 'a8', 'e4', 'c1', 'd5', 'e1', 'c6', 'd1']))
        self.assertEqual(get_pos('QUEEN','f8'), set(['g7', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'h6', 'h8', 'g8',
                                                     'b4', 'a3', 'c8', 'e8', 'd8', 'd6', 'a8', 'e7', 'b8', 'c5']))

    def test_get_king_pos(self):
        self.assertEqual(get_pos('KING','g5'), set(['g6', 'g4', 'f4', 'f5', 'f6', 'h6', 'h4', 'h5']))
        self.assertEqual(get_pos('KING','d2'), set(['c3', 'c2', 'c1', 'd1', 'e1', 'd3', 'e3', 'e2']))
        self.assertEqual(get_pos('KING','g1'), set(['h2', 'f1', 'f2', 'h1', 'g2']))
        self.assertEqual(get_pos('KING','h1'), set(['h2', 'g2', 'g1']))
        self.assertEqual(get_pos('KING','f8'), set(['g7', 'e7', 'g8', 'e8', 'f7']))

    def test_get_knight_pos(self):
        self.assertEqual(get_pos('KNIGHT','g5'), set(['f3', 'f7', 'h3', 'h7', 'e4', 'e6']))
        self.assertEqual(get_pos('KNIGHT','d2'), set(['f1', 'f3', 'b1', 'b3', 'e4', 'c4']))
        self.assertEqual(get_pos('KNIGHT','g1'), set(['h3', 'f3', 'e2']))
        self.assertEqual(get_pos('KNIGHT','h1'), set(['f2', 'g3']))
        self.assertEqual(get_pos('KNIGHT','f8'), set(['g6', 'e6', 'h7', 'd7']))


if __name__ == '__main__':
    unittest.main()

