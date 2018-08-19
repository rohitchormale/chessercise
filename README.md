# Chessercise


## Usage
python chessercise.py --piece KNIGHT --position d2


## Help
python chessercise.py --help

## Tests
python test_chessercise.py

## Terminologies
- course(str) 
direction to traverse. possible values - TOP, RIGHT, BOTTOM, LEFT, RTOP, LTOP, RBOTTOM, LBOTTOM

- squares (int)
number of squres to traverls

- posf (str)
file value of given position

- posr (int)
rank value of given position

- exact (bool)
In case boundry is crossed when traversing, return zero positions if True. If False, when boundry is crossed, return all traversed positions till boundry.


## Notes
This module implements various APIs to find potential positions for given chess piece to advance, assuming no other piece
on board. There are 3 core apis,
1. linear_traverse -- Traverse board in linear fashion from given position and produce possible positions
2. diagonal_traverse -- Traverse board in diagonal fashion from given position and produce possible positions 
3. compound_traverse -- Traverse board by chaining different paths together using very basic DSL

