from board import Board
from const import *
import sys
from square import Square
import pygame
import pyautogui

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
        cols = {
            "a" : 1, 
            "b" : 2,
            "c" : 3,
            "d" : 4,
            "e" : 5,
            "f" : 6,
            "g" : 7,
            "h" : 8
        }

        move = str(move)

        initial = (cols[move[0]], ROWS - int(move[1]))
        final = (cols[move[2]], ROWS - int(move[3]))
        x,y = (GAP + initial[0] * SQSIZE) - SQSIZE//2, (GAP + initial[1] * SQSIZE) + SQSIZE//2

        pygame.mouse.set_pos(x,y)
        x,y = (GAP + final[0] * SQSIZE) - SQSIZE//2, (GAP + final[1] * SQSIZE) + SQSIZE//2
        pyautogui.click(button='right', clicks=20, interval=1)
        pygame.mouse.set_pos(x,y)
        
        
        # autopy.mouse.smooth_move(200,200)

        # click
        # release
        pass