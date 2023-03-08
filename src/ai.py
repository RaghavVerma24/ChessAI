from board import Board
from const import *

class Ai:

    def __init__(self):
        self.board = Board()
        pass

    def minimax(self):
        # params: board (includes child elements), alpha, beta, depth = 3, player (white or black)
        # For each board loop through the child boards and get a herustic evalution (get number of points on board) and alternative between min and max until you reach the current tree node for the board
        pass

    def heuristic(self):
        # params: board, maximizing color
        # determine how good a position is for a slect player

        pieces = {
            "pa": 1,
            "ro": 5,
            "kn": 3,
            "bi": 3,
            "qu": 9,
            "ki": 1000,
        }

        white_eval = 0
        black_eval = 0
        board = self.board.see_board()
        for row in range(ROWS):
            for col in range(COLS):
                if board[row][col][0] == "b":
                    black_eval += pieces[board[row][col][1:3]]
                elif board[row][col][0] == "w":
                    white_eval += pieces[board[row][col][1:3]]
                else:
                    continue
        
        print(black_eval,white_eval)