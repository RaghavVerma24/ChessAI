import pygame
from const import *
from board import Board
from dragger import Dragger
from square import Square
from piece import *


class Game:

    def __init__(self):
        self.next_player = 'white'
        self.hovered_sqr = None
        self.board = Board()
        self.dragger = Dragger()
        self.boardCol = ["a", "b", "c", "d", "e", "f", "g", "h"]

    def show_position(self, surface):
        for row in range(ROWS):
            self.text(surface, str(ROWS-row), GAP + 10, GAP + 15 + row*SQSIZE, 16, (234, 235, 200) if row % 2 else (119, 154, 88))
        for col in range(COLS):
            self.text(surface, self.boardCol[col], GAP + (SQSIZE - 15 + col*SQSIZE), GAP + SQSIZE - 15 + 7*SQSIZE, 18, (119, 154, 88) if col % 2 else (234, 235, 200))

    def text(self, screen, img_text, x, y, size, color):
        font = pygame.font.Font('freesansbold.ttf', size)
        text = font.render(img_text,
                           True, color)
        textRect = text.get_rect()
        textRect.center = (x, y)

        screen.blit(text, textRect)

    def show_bg(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                if (row+col) % 2 == 0:
                    color = (234, 235, 200)
                else:
                    color = (119, 154, 88)

                rect = (GAP + col * SQSIZE,GAP + row * SQSIZE, SQSIZE, SQSIZE)

                pygame.draw.rect(surface, color, rect)
        self.show_position(surface)
        

    def show_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece

                    # all pieces but the piece being dragged
                    if piece is not self.dragger.piece:
                        piece.set_sprite(size=80)
                        img = pygame.image.load(piece.sprite)
                        img_center = GAP + col * SQSIZE + SQSIZE // 2, GAP + row * SQSIZE + SQSIZE // 2
                        piece.sprite_rect = img.get_rect(center=img_center)
                        surface.blit(img, piece.sprite_rect)

    def show_moves(self, surface):
        if self.dragger.dragging:
            piece = self.dragger.piece

            # get all valid moves
            for move in piece.moves:
                color = '#C86464' if (move.final.row + move.final.col) % 2 == 0 else '#C86646'
                rect = (GAP + move.final.col * SQSIZE, GAP + move.final.row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)

    def show_last_move(self, surface):
        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final

            for pos in [initial, final]:
                color = (244, 247, 116) if (pos.row + pos.col) % 2 == 0 else (172, 195, 51)
                rect = (GAP + pos.col * SQSIZE, GAP + pos.row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)

    def show_hover(self, surface):
        if self.hovered_sqr:
            color = (180, 180, 180)
            rect = (GAP + (self.hovered_sqr.col * SQSIZE), GAP + (self.hovered_sqr.row * SQSIZE), SQSIZE, SQSIZE)
            pygame.draw.rect(surface, color, rect, width=3)

    def show_timer(self, surface):
        

    def next_turn(self, ai_starting):
        self.next_player = 'white' if self.next_player == 'black' else 'black'
        

    def set_hover(self, row, col):
        try:
            self.hovered_sqr = self.board.squares[row][col]
        except:
            pass
    
    def reset(self):
        self.__init__()

    