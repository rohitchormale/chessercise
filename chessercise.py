#!/usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = 'Rohit Chormale'


"""
This module implements various APIs to find potential positions for given chess piece to advance, assuming no other piece
on board. There are 3 core apis,
1. linear_traverse -- Traverse board in linear fashion from given position and produce possible positions
2. diagonal_traverse -- Traverse board in diagonal fashion from given position and produce possible positions 
3. compound_traverse -- Traverse board by chaining different paths together using very basic DSL


Terminologies:
- course (str) 
direction to traverse. possible values - TOP, RIGHT, BOTTOM, LEFT, RTOP, LTOP, RBOTTOM, LBOTTOM

- squares (int)
number of squres to traverls

- posf (str)
file value of given position

- posr (int)
rank value of given position

- exact (bool)
In case boundry is crossed when traversing, return zero positions if True. If False, when boundry is crossed, return all traversed positions till boundry.


Usage:
python chessercise.py --piece KNIGHT --position d2

Help:
python chessercise.py --help

Tests:
python test_chessercise.py

"""


LOWER_LIMIT = 1
UPPER_LIMIT = 8
FILES = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8}
REVERSE_FILES = {v: k for k, v in FILES.items()} 


def linear_traverse(posf, posr, course, squares=UPPER_LIMIT, exact=False):
    """Traverse chess board linearly.

    This function can be used to traverse board in linear fashion to calculate possible positions.

    Args:
        course : Direction to traverse. Possible values are ['TOP', 'RIGHT', 'LEFT', 'BOTTOM']
        posf : file of position. Possible values are [ 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        posr : rank of position. Possible values are [1, 2, 3, 4, 5, 6, 7, 8]
        squares : number of squares to traverse
        exact : Boolean. During traversing if board is crossed, return empty list if True. But if False, return
                all traversed positions even count of squares is invalid. e.g. if route is  ('f8', 'RIGHT', 3), only 2 squares
                can be traversed. If `exact=False`, output will be ['g8', 'h8'] but if `exact=True`, output will be [] as
                board is crossed.

    Returns:
        list of traversed positions
    """
    all_pos = []

    def _get_pos(pos):
        if len(all_pos) >= squares:
            return all_pos

        if course in ('TOP', 'RIGHT'):
            npos = pos + 1
            if npos > UPPER_LIMIT:
                if exact:
                    return []
                return all_pos
        else:
            npos = pos - 1
            if npos < LOWER_LIMIT:
                if exact:
                    return []
                return all_pos

        if course in ('LEFT', 'RIGHT'):
            all_pos.append(REVERSE_FILES[npos]+str(posr))
        else:
            all_pos.append(posf+str(npos))
        return _get_pos(npos)

    if course in ('LEFT', 'RIGHT'):
        return _get_pos(FILES[posf])
    return _get_pos(posr)


def diagonal_traverse(posf, posr, course, squares=UPPER_LIMIT, exact=False):
    """Traverse chess board diagonally.

    This function can be used to traverse board in diagonal fashion to calculate posibble positions.

    Args:
        course : Direction to traverse. Possible values are ['RTOP', 'LTOP', 'RBOTTOM', 'LBOTTOM']
        posf : file of position. Possible values are ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        posr : rank of position. Possible values are [1, 2, 3, 4, 5, 6, 7, 8]
        squares : number of squares to traverse
        exact : Boolean. During traversing if board is crossed, return empty list if True. But if False, return
                all traversed positions even endpoint is invalid. e.g. if route is  ('e7', 'LTOP', 3), then only 1 square
                can be traversed. If `exact=False`, output will be ['f8'] but if `exact=True`, output will be [] as
                board is crossed.

    Returns:
        list of traversed positions
    """
    all_pos = []

    def _get_pos(posf, posr):
        if len(all_pos) >= squares:
            return all_pos

        if course == 'LTOP':
            nposf = posf - 1
            nposr = posr + 1
            if nposf < LOWER_LIMIT or nposr > UPPER_LIMIT:
                if exact:
                    return []
                return all_pos

        elif course == 'RTOP':
            nposf = posf + 1
            nposr = posr + 1
            if nposf > UPPER_LIMIT or nposr > UPPER_LIMIT:
                if exact:
                    return []
                return all_pos

        elif course == 'LBOTTOM':
            nposf = posf - 1
            nposr = posr - 1
            if nposf < LOWER_LIMIT or nposr < LOWER_LIMIT:
                if exact:
                    return []
                return all_pos
        else:
            nposf = posf + 1
            nposr = posr - 1
            if nposf > UPPER_LIMIT or nposr < LOWER_LIMIT:
                if exact:
                    return []
                return all_pos

        all_pos.append(REVERSE_FILES[nposf]+str(nposr))
        return _get_pos(nposf, nposr)

    return _get_pos(FILES[posf], posr)


def compound_traverse(posf, posr, path, exact=False):
    """Traverse chess board.

    This function can be used to chain paths for traversing chess board.

    Args:
        posf : file of position. Possible values are ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        posr : rank of position. Possible values are [1, 2, 3, 4, 5, 6, 7, 8]
        path : list of tuples in format [(COURSE, SQUARES), (COURSE, SQUARES) ...] e.g. [('TOP', 3), ('RBOTTOM', 1), ('LBOTTOM', 2)].
                This list will be traversed sequentially.
        exact : Boolean. During traversing if board is crossed, return empty list if True. But if False, return
                all traversed positions even endpoint is invalid. e.g. Suppose, initial positions is 'd2' and path to traverse is
                [('BOTTOM', 3), ('LTOP', 3)]. Now, if `exact=False`, first route will be traversed to only 1 square and then
                next route will be traversed. So output will be ['d1', 'c2', 'b3', 'a4']. But if `exact=True`, in this case,
                output will be [] as board will be crossed on first path.

    Returns:
        list of traversed positions
    """
    all_pos = []

    def _get_pos(posf, posr, route):
        try:
            course = route[0]
            squares = route[1]
        except IndexError:
            return all_pos

        if course in ("TOP", "BOTTOM", "LEFT", "RIGHT"):
            positions = linear_traverse(posf, posr, course, squares, exact)
        else:
            positions = diagonal_traverse(posf, posr, course, squares, exact)

        if not positions:
            if exact:
                return []
            return all_pos

        all_pos.extend(positions)
        if not path:
            return all_pos

        next_pos = positions.pop()
        next_route = path.pop(0)
        return _get_pos(next_pos[0], int(next_pos[1]), next_route)

    if path:
        return _get_pos(posf, posr, path.pop(0))
    return []


def get_pos(piece, pos):
    """Get possible positions to advance for given piece, from given positions.

    Args:
        piece : ROOK, BISHOP, PAWN, KING, QUEEN, KNIGHT
        pose : initial piece position on chess board in Algebric notation e.g. a4, g5, d3

    Returns:
        list of possible positions to advance
    """
    paths = {
        'ROOK': [[('TOP', UPPER_LIMIT)], [('BOTTOM', UPPER_LIMIT)], [('LEFT', UPPER_LIMIT)], [('RIGHT', UPPER_LIMIT)]],
        'BISHOP': [[('LTOP', UPPER_LIMIT)], [('RTOP', UPPER_LIMIT)], [('LBOTTOM', UPPER_LIMIT)], [('RBOTTOM', UPPER_LIMIT)]],
        'PAWN': [[('TOP', 1)], [('RTOP', 1)], [('LTOP', 1)]],
        'KING': [[('TOP',1)], [('BOTTOM', 1)], [('LEFT', 1)], [('RIGHT', 1)], [('RTOP', 1)], [('LTOP', 1)], [('RBOTTOM', 1)], [('LBOTTOM', 1)]],
        'QUEEN': [[('TOP', UPPER_LIMIT)], [('BOTTOM', UPPER_LIMIT)], [('LEFT', UPPER_LIMIT)], [('RIGHT', UPPER_LIMIT)],
                  [('LTOP', UPPER_LIMIT)], [('RTOP', UPPER_LIMIT)], [('LBOTTOM', UPPER_LIMIT)], [('RBOTTOM', UPPER_LIMIT)]],
        'KNIGHT': [[('RTOP', 1), ('TOP', 1)], [('RTOP', 1), ('RIGHT', 1)], [('RBOTTOM', 1), ('RIGHT', 1)], [('RBOTTOM', 1), ('BOTTOM', 1)],
        [('LTOP', 1), ('TOP', 1)], [('LTOP', 1), ('LEFT', 1)], [('LBOTTOM', 1), ('BOTTOM', 1)], [('LBOTTOM', 1), ('LEFT', 1)],],
    }

    posf = pos[0]
    posr = int(pos[1])
    all_pos = []

    if piece not in paths:
        return all_pos
    if posf not in FILES:
        return
    if posr not in REVERSE_FILES:
        return

    if piece == 'KNIGHT':
        # for KNIGHT, we only need endpoints as positions are not sequential
        for path in paths[piece]:
            pt = compound_traverse(posf, posr, path=path, exact=True)
            if pt: all_pos.append(pt[-1])
    else:
        for path in paths[piece]:
            pos = compound_traverse(posf, posr, path, exact=False)
            all_pos.extend(pos)
    return set(all_pos)


if __name__ == '__main__':
    import argparse, sys
    ap = argparse.ArgumentParser(description="Chessercise - Find possible positions on chess board")
    ap.add_argument("--piece", help="Chess Piece from PAWN/ROOK/BISHOP/KNIGHT/QUEEN/KING")
    ap.add_argument("--position", help="Postion on chess board in Algebric notation e.g. a5")
    args = vars(ap.parse_args())
    piece = args['piece']
    position = args['position']
    if piece not in ('PAWN', 'ROOK', 'BISHOP', 'KING', 'QUEEN', 'KNIGHT') or position is None or \
            len(position) != 2 or position[0] not in FILES or int(position[1]) not in REVERSE_FILES:
        ap.print_help()
        sys.exit(1)
    all_pos = get_pos(args['piece'], args['position'])
    if all_pos:
        print("Possible Positions | %s" % ', '.join(all_pos))
    else:
        print("Possible Positions | None")
    sys.exit()



