from const import *
from square import Square
from piece import *
from move import Move
import copy

class Board:

    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]
        self.last_move = None
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')

    def move(self, piece, move, testing = False):
        initial = move.initial
        final = move.final

        # update console board move
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece

        # pawn promotion
        if piece.name == 'pawn':
            self.check_promotion(piece, final)

        # castle king
        if piece.name == 'king':
            if self.castling(initial, final) and not testing:
                diff = final.col - initial.col
                rook = piece.left_rook if (diff < 0) else piece.right_rook
                self.move(rook, rook.moves[-1])

        # move on board
        piece.moved = True

        # clear valid moves
        piece.clear_moves()

        # set last move
        self.last_move = move

    def valid_move(self, piece, move):
        return move in piece.moves

    def check_promotion(self, piece, final):
        if final.row == 0 or final.row == 7:
            self.squares[final.row][final.col].piece = Queen(piece.color)

    def castling(self, initial, final):
        return abs(initial.col - final.col) == 2

    def in_check(self, piece, move):
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self)
        temp_board.move(temp_piece, move, testing=True)

        for row in range(ROWS):
            for col in range(COLS):
                if temp_board.squares[row][col].has_rival_piece(piece.color):
                    attacking_piece = temp_board.squares[row][col].piece
                    temp_board.calc_moves(attacking_piece, row, col, bool=False)

                    for attacking_move in attacking_piece.moves:
                        if isinstance(attacking_move.final.piece, King):

                            attacking_color = attacking_piece.color
                            # calc moves of all opposing color pieces (attacking color)
                            # color_piece = self.squares[0][2].piece
                            # temp_board.calc_moves(color_piece, 0, 2, bool=False)
                            # color_piece.all_moves()                            

                            return True

        return False

    def checkmate(self):
        pass

    def calc_moves(self, piece, row, col, bool=True):

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
                        # check for next move check
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_move(move)
                        else:
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
                        final_piece = self.squares[move_row][move_col].piece
                        final = Square(move_row, move_col, final_piece)
                        # create the new move
                        move = Move(initial, final)
                        # check for next move check
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_move(move)
                        else:
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
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        # create new move
                        move = Move(initial, final)
                        # check for next move check
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_move(move)
                            else:
                                break
                        else:
                            # append new move
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
                        final_piece = self.squares[move_row][move_col].piece
                        final = Square(move_row,move_col, final_piece)
                        # create new move
                        move = Move(initial, final)

                        # empty
                        if self.squares[move_row][move_col].isempty():
                            # check for next move check
                            if bool:
                                if not self.in_check(piece, move):
                                    # append new move
                                    piece.add_move(move)
                            else:
                                # append new move
                                piece.add_move(move)  

                        # has enemy piece
                        elif self.squares[move_row][move_col].has_rival_piece(piece.color):
                            # check for next move check
                            if bool:
                                if not self.in_check(piece, move):
                                    # append new move
                                    piece.add_move(move)
                            else:
                                # append new move
                                piece.add_move(move)
                            break
                        
                        # has team piece
                        elif self.squares[move_row][move_col].has_team_piece(piece.color):
                            break
                    
                    # out of range
                    else:
                        break

                    # incrementing the number of squares for movement
                    move_row, move_col = move_row + row_incr, move_col + col_incr,

        def king_moves():
            adjs = [
                (row-1,col),
                (row-1,col+1),
                (row,col+1),
                (row+1,col+1),
                (row+1,col),
                (row+1,col-1),
                (row,col-1),
                (row-1,col-1),
            ]

            # normal move
            for possible_move in adjs:
                move_row, move_col = possible_move

                if Square.in_range(move_row,move_col):
                    if self.squares[move_row][move_col].isempty_or_rival(piece.color):
                        # create squares for new move
                        initial = Square(row, col)
                        final = Square(move_row, move_col)
                        # create new move
                        move = Move(initial, final)
                        # check for next move check
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_move(move)
                            else:
                                break
                        else:
                            # append new move
                            piece.add_move(move)

            # castling moves
            if not piece.moved:

                # king castling
                right_rook = self.squares[row][7].piece
                if right_rook.name == 'rook':
                    if not right_rook.moved:
                        for c in range(5,7):
                            if self.squares[row][c].has_piece():
                                break

                            if c == 6:
                                piece.right_rook = right_rook

                                # rook move
                                initial = Square(row, 7)
                                final = Square(row, 5)
                                moveRook = Move(initial, final)

                                # king move
                                initial = Square(row, col)
                                final = Square(row, 6)
                                moveKing = Move(initial, final)

                                # check for next move check
                                if bool:
                                    if not self.in_check(piece, moveKing) and self.in_check(right_rook, moveRook):
                                        # append new rook move
                                        right_rook.add_move(moveRook)
                                        # append new move king
                                        piece.add_move(moveKing)
                                else:
                                    # append new rook move
                                    right_rook.add_move(moveRook)
                                    # append new move King 
                                    piece.add_move(moveKing)

                # queen castling
                left_rook = self.squares[row][0].piece
                if left_rook.name == 'rook':
                    if not left_rook.moved:
                        for c in range(1,4):
                            if self.squares[row][c].has_piece():
                                break

                            if c == 3:
                                piece.left_rook = left_rook

                                # rook move
                                initial = Square(row, 0)
                                final = Square(row, 3)
                                left_rook = Move(initial, final)

                                # king move
                                initial = Square(row, col)
                                final = Square(row, 2)
                                moveKing = Move(initial, final)

                                # check for next move check
                                if bool:
                                    if not self.in_check(piece, moveKing) and self.in_check(left_rook, moveRook):
                                        # append new rook move
                                        left_rook.add_move(moveRook)
                                        # append new move king
                                        piece.add_move(moveKing)
                                else:
                                    # append new rook move
                                    left_rook.add_move(moveRook)
                                    # append new move King 
                                    piece.add_move(moveKing)

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
            king_moves()
    
    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)

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
