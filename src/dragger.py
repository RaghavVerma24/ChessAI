import pygame
from const import *
from piece import Piece

class Dragger:

    def __init__(self):
        self.piece = None
        self.dragging = False
        self.mouseX = 0
        self.mouseY = 0
        self.initial_row = 0
        self.initial_col = 0

    def update_blit(self, surface):
        # set size
        self.piece.set_sprite(size= 80)
        texture = self.piece.sprite
        # get piece
        img = pygame.image.load(texture)
        # blit piece
        img_center = (self.mouseX, self.mouseY)
        self.piece.sprite_rect = img.get_rect(center=img_center)
        # blit
        surface.blit(img, self.piece.sprite_rect)

    def update_mouse(self, pos):
        self.mouseX, self.mouseY = pos

    def save_initial(self, pos):
        self.initial_row = (pos[1] - GAP) // SQSIZE
        self.initial_col = (pos[0] - GAP) // SQSIZE

    def drag_piece(self, piece):
        self.piece = piece
        self.dragging = True

    def undrag_piece(self):
        self.piece = None
        self.dragging = False