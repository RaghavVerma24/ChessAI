from const import *
from square import Square
from piece import *
from move import Move


class Board:

    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]

        self._create()
        self._add_pieces('white')
        self._add_pieces('black')

    # Find all valid moves for a piece at a specific position

    def calc_moves(self, piece, row, col):

        def pawn_moves():
            steps = 1 if piece.moved else 2

            # vertical moves
            start = row + piece.dir
            end = row + piece.dir * (1 + steps)
            for move_row in range(start, end, piece.dir):
                if Square.in_range(move_row):
                    if self.squares[move_row][col].isempty():
                        # create initial and final move squares
                        initial = Square(row, col)
                        final = Square(move_row, col)
                        # create the new move
                        move = Move(initial, final)
                        # append new move
                        piece.add_move(move)
                    # blocked by another piece
                    else:
                        break
                # not in range
                else:
                    break

            # diagonal moves
            move_row = row + piece.dir
            move_cols = [col-1, col+1]
            for move_col in move_cols:
                if Square.in_range(move_row, move_col):
                    if self.squares[move_row][move_col].has_rival_piece(piece.color):
                        # create initial and final move squares
                        initial = Square(row, col)
                        final = Square(move_row, move_col)
                        # create the new move
                        move = Move(initial, final)
                        # append new move
                        piece.add_move(move)

        def knight_moves():
            # 8 possible moves
            possible_moves = [
                (row-2, col+1),
                (row-1, col+2),
                (row+1, col+2),
                (row+2, col+1),
                (row+2, col-1),
                (row+1, col-2),
                (row-1, col-2),
                (row-2, col-1),
            ]

            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_rival(piece.color):
                        # create squares for new move
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        # create new move
                        move = Move(initial, final)
                        # append
                        piece.add_move(move)

        def straightline_moves(incrs):
            for incr in incrs:
                row_incr, col_incr = incr
                move_row = row + row_incr
                move_col = col + col_incr

                while True:
                    if Square.in_range(move_row, move_col):
                        # create Square for new move
                        initial = Square(row, col)
                        final = Square(move_row,move_col)
                        # create new move
                        move = Move(initial, final)

                        # empty
                        if self.squares[move_row][move_col].isempty():
                            # append new move
                            piece.add_move(move)

                        # has enemy piece
                        if self.squares[move_row][move_col].has_rival_piece(piece.color):
                            # append new move
                            piece.add_move(move)
                            break
                        
                        # has team piece
                        if self.squares[move_row][move_col].has_team_piece(piece.color):
                            break
                    
                    # out of range
                    else:
                        break

                    # incrementing the number of squares for movement
                    move_row, move_col = move_row + row_incr, move_col + col_incr,

        if piece.name == 'pawn':
            pawn_moves()
        elif piece.name == 'knight':
            knight_moves()
        elif piece.name == 'bishop':
            straightline_moves([(-1,1),(-1,-1),(1,1),(1,-1)])
        elif piece.name == 'rook':
            straightline_moves([(-1,0),(0,1),(1,0),(0,-1)])
        elif piece.name == 'queen':
            straightline_moves([(-1,1),(-1,-1),(1,1),(1,-1),(-1,0),(0,1),(1,0),(0,-1)])
        elif piece.name == 'king':
            pass
        


    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)

    # Create chess pieces
    def _add_pieces(self, color):
        if color == 'white':
            row_pawn, row_other = (6, 7)
        else:
            row_pawn, row_other = (1, 0)

        # pawns
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))

        # knights
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        # bishops
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

        # rooks
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))

        # queen
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))

        # king
        self.squares[row_other][4] = Square(row_other, 4, King(color))
