from board import Board
from const import *
import sys

class Ai:

    def __init__(self):
        self.board = Board()
        pass

    def minimax(self, board, alpha, beta, maximizing_player, depth = 3):
        # params: board (includes child elements), alpha, beta, depth = 3, player (white or black)
        # For each board loop through the child boards and get a herustic evalution (get number of points on board) and alternative between min and max until you reach the current tree node for the board
        pass

    def heuristic(self, board, depth=3, maximizingPlayer="white"):
        if depth == 0:
            return self.evaluate_board(board)
        
        if maximizingPlayer:
            maxEval = - sys.maxsize - 1
            # for each child in board
            #
        
        else:
            minEval = sys.maxsize
        # params: board, maximizing color
        # determine how good a position is for a slect player
        pass


    def evaluate_board(self, board):
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
        for row in range(ROWS):
            for col in range(COLS):
                if board[row][col][0] == "b":
                    black_eval += pieces[board[row][col][1:3]]
                elif board[row][col][0] == "w":
                    white_eval += pieces[board[row][col][1:3]]
                else:
                    continue
        
        return white_eval-black_eval