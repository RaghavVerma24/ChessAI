import pygame
import sys

from const import *
from game import Game
from square import Square
from move import Move
from db import Db
from ai import Ai

import pygame_widgets
from pygame_widgets.button import Button
from pygame_widgets.textbox import TextBox


class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Chess')
        self.game = Game()
        self.db = Db()
        self.ai = Ai()
        self.starting = True
        self.background = (49, 46, 43)
        self.ai_starting = False

    def starting_screen(self, screen):
        screen.fill(self.background)
        self.text(screen, 'Play Chess Online or with AI', WIDTH // 2, (HEIGHT // 2) - 100, 32)

        # self.button(screen, 250, 70, "Play with Player", (127, 166,
        #             80), (149, 187, 74), btn_seperator=0)
        # self.button(screen, 250, 70, "Play with AI",
        #             (56, 54, 52), (74, 72, 70))
        human = pygame.draw.rect(screen, (127, 166, 80), pygame.Rect(275, 365, 250, 70))

        ai = pygame.draw.rect(screen, (56, 54, 52), pygame.Rect(275, 455, 250, 70))


        if human.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, (149, 187, 74), pygame.Rect(275, 365, 250, 70))

        if ai.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, (74, 72, 70), pygame.Rect(275, 455, 250, 70))

        
        self.text(screen, 'Play with Player', WIDTH // 2, (HEIGHT // 2), 24)
        self.text(screen, 'Play with AI', WIDTH // 2, (HEIGHT // 2) + 90, 24)
        

    def text(self, screen, img_text, x, y, size):
        font = pygame.font.Font('freesansbold.ttf', size)
        text = font.render(img_text,
                           True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = (x, y)

        screen.blit(text, textRect)

    def mainloop(self):
        screen = self.screen
        game = self.game
        board = self.game.board
        dragger = self.game.dragger
        db = self.db
        ai = self.ai

        db.get_plays()

        while True:
            if self.starting:
                self.starting_screen(screen)
            elif not self.starting and self.ai_starting:
                # ai.heuristic()
                game.show_bg(screen)
                game.show_last_move(screen)
                game.show_moves(screen)
                game.show_pieces(screen)
                game.show_hover(screen)

                if dragger.dragging:
                    dragger.update_blit(screen)

            else:
                game.show_bg(screen)
                game.show_last_move(screen)
                game.show_moves(screen)
                game.show_pieces(screen)
                game.show_hover(screen)

                if dragger.dragging:
                    dragger.update_blit(screen)

            for event in pygame.event.get():
                if self.starting:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse = pygame.mouse.get_pos()
                        if self.starting:
                            if 275 <= mouse[0] <= 525 and 365 <= mouse[1] <= 435:
                                self.starting = False
                            elif 275 <= mouse[0] <= 525 and 455 <= mouse[1] <= 525:
                                self.starting = False
                                self.ai_starting = True

                # click piece
                else:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        dragger.update_mouse(event.pos)

                        clicked_row = dragger.mouseY // SQSIZE
                        clicked_col = dragger.mouseX // SQSIZE

                        # Check if game square has a piece
                        if board.squares[clicked_row][clicked_col].has_piece():
                            piece = board.squares[clicked_row][clicked_col].piece

                            # find next player turn
                            if piece.color == game.next_player:
                                board.calc_moves(
                                    piece, clicked_row, clicked_col, bool=True)
                                dragger.save_initial(event.pos)
                                dragger.drag_piece(piece)

                                game.show_bg(screen)
                                game.show_last_move(screen)
                                game.show_moves(screen)
                                game.show_pieces(screen)

                    # move piece
                    elif event.type == pygame.MOUSEMOTION:
                        motion_row = event.pos[1] // SQSIZE
                        motion_col = event.pos[0] // SQSIZE

                        game.set_hover(motion_row, motion_col)

                        if dragger.dragging:
                            dragger.update_mouse(event.pos)
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)
                            game.show_hover(screen)
                            dragger.update_blit(screen)

                    # release piece
                    elif event.type == pygame.MOUSEBUTTONUP:

                        if dragger.dragging:
                            dragger.update_mouse(event.pos)

                            released_row = dragger.mouseY // SQSIZE
                            released_col = dragger.mouseX // SQSIZE

                            # create possible move
                            initial = Square(
                                dragger.initial_row, dragger.initial_col)
                            final = Square(released_row, released_col)
                            move = Move(initial, final)

                            # check valid move
                            if board.valid_move(dragger.piece, move):
                                board.move(dragger.piece, move)
                                ai.heuristic(board.see_board())
                                # draw piece on board
                                game.show_bg(screen)
                                game.show_last_move(screen)
                                game.show_pieces(screen)
                                # next turn
                                game.next_turn()

                        dragger.undrag_piece()
                        board.all_possible_moves(game.next_player)
                        board.create_child_boards()

                        # board.generate_moves_ai()

                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            game.reset()
                            game = self.game
                            board = self.game.board
                            dragger = self.game.dragger
                        if event.key == pygame.K_q:
                            self.starting = True
                            game.reset()
                            game = self.game
                            board = self.game.board
                            dragger = self.game.dragger

                # quit app
                if (event.type == pygame.QUIT):
                    pygame.quit()
                    sys.exit()

            pygame_widgets.update(pygame.event.get())
            pygame.display.update()


main = Main()
main.mainloop()
