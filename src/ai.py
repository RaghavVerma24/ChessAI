from board import Board
from const import *
import sys
from square import Square


class Ai:

    def __init__(self):
        self.board = Board()
        pass

    def minimax(self, children, board, depth, maximizingPlayer):
        children = list(children)
        
        if depth == 0:
            return self.heuristic(board)
        
        if maximizingPlayer:
            maxEval = - sys.maxsize - 1
            for i in range(len(children)):
                eval = self.minimax(children[i], board, depth - 1, False)
                maxEval = max(maxEval, eval)
            return maxEval
        
        else:
            minEval = sys.maxsize
            for i in range(len(children)):
                eval = self.minimax(children[i], board, depth - 1, True)
                minEval = min(minEval, eval)
            return minEval

        # params: board, maximizing color
        # determine how good a position is for a slect player=

    def heuristic(self, board):
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
    
    def make_move(self, screen, move):
        print(move)
        # move mouse 
        # click
        # release
        pass