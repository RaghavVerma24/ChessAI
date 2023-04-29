import pygame
import sys
import chess

from const import *
from game import Game
from square import Square
from move import Move
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
        self.ai = Ai()
        self.starting = True
        self.background = (49, 46, 43)
        self.ai_starting = False
        self.gameover = False
        self.winner = ""
        self.winnerColor = ""
        self.ai_move = True
        self.start_time = 0
        self.chessBoard = chess.Board()
        self.released = ()

    def end_game(self, screen, winner):
        pygame.time.delay(500)
        
        screen.fill(self.background)
        self.text(screen, f"The Winner is {winner}", WIDTH // 2, (HEIGHT // 2) - 100, 32)

        play_again = pygame.draw.rect(screen, (127, 166, 80), pygame.Rect(275, 365, 250, 70))

        if play_again.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, (149, 187, 74), pygame.Rect(275, 365, 250, 70))
            self.gameover = False

        self.text(screen, 'Play Again', WIDTH // 2, (HEIGHT // 2), 24)

    def starting_screen(self, screen):
        screen.fill(self.background)
        self.text(screen, 'Play Chess Online or with AI', WIDTH // 2, (HEIGHT // 2) - 100, 32)

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
        ai = self.ai

        while True:
            if self.gameover:
                self.end_game(screen, self.winnerColor)
                self.winner = "True"
                self.chessBoard = chess.Board()                
            else:
                if (self.winner != "True"):
                    if self.starting:
                        self.start_time = pygame.time.get_ticks()//1000
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
                        game.show_timer(screen, self.start_time)
                        game.show_bg(screen)
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        game.show_hover(screen)

                        if dragger.dragging:
                            dragger.update_blit(screen)

                for event in pygame.event.get():
                    if self.ai_starting and self.ai_move:
                        print(self.chessBoard.legal_moves)
                        print("Game Score: ", board.heuristic())
                            # ai.make_move(screen, list(self.chessBoard.legal_moves)[0], self.released)
                        board.create_child_boards(self.chessBoard, False)
                        # ai.minimax(board.children, board, 3, True) 
                        self.ai_move = False
                    if self.starting or self.winner != "":
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            mouse = pygame.mouse.get_pos()
                            if self.starting or self.winner != "":
                                if 275 <= mouse[0] <= 525 and 365 <= mouse[1] <= 435:
                                    if (self.winner != ""):
                                        game.reset()
                                        game = self.game
                                        board = self.game.board
                                        dragger = self.game.dragger
                                        self.gameover = False
                                        self.winner = ""
                                        self.starting = True
                                    else:
                                        self.starting = False
                                        pygame.time.delay(500)

                                elif 275 <= mouse[0] <= 525 and 455 <= mouse[1] <= 525:
                                    self.starting = False
                                    self.ai_starting = True

                    # click piece
                    else:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if((event.pos[0] >= GAP + 35) and (event.pos[0] <= WIDTH - GAP - 35)):
                                if((event.pos[1] >= GAP + 35) and (event.pos[1] <= HEIGHT - GAP - 35)):
                                    dragger.update_mouse(event.pos)

                                    clicked_row = (dragger.mouseY - GAP) // SQSIZE
                                    clicked_col = (dragger.mouseX - GAP) // SQSIZE

                                    # Check if game square has a piece
                                    try:
                                        if board.squares[clicked_row][clicked_col].has_piece():
                                            piece = board.squares[clicked_row][clicked_col].piece

                                            # find next player turn
                                            try:
                                                if piece.color == game.next_player:
                                                    board.calc_moves(
                                                        piece, clicked_row, clicked_col, bool=True)
                                                    dragger.save_initial(event.pos)
                                                    dragger.drag_piece(piece)

                                                    game.show_bg(screen)
                                                    game.show_last_move(screen)
                                                    game.show_moves(screen)
                                                    game.show_pieces(screen)
                                            except:
                                                pass
                                    except:
                                        pass

                        # move piece
                        elif event.type == pygame.MOUSEMOTION:
                            motion_row = (event.pos[1] - GAP) // SQSIZE
                            motion_col = (event.pos[0] - GAP) // SQSIZE

                            game.set_hover(motion_row, motion_col)

                            if dragger.dragging:
                                if((event.pos[0] >= GAP + 35) and (event.pos[0] <= WIDTH - GAP - 35)):
                                    if((event.pos[1] >= GAP + 35) and (event.pos[1] <= HEIGHT - GAP - 35)):
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
                                if((event.pos[0] >= GAP + 35) and (event.pos[0] <= WIDTH - GAP - 35)):
                                    if((event.pos[1] >= GAP + 35) and (event.pos[1] <= HEIGHT - GAP - 35)):
                                        dragger.update_mouse(event.pos)

                                        released_row = (dragger.mouseY - GAP) // SQSIZE
                                        released_col = (dragger.mouseX - GAP) // SQSIZE
                                        self.released = (released_col, released_row)

                                        # create possible move
                                        initial = Square(
                                            dragger.initial_row, dragger.initial_col)
                                        final = Square(released_row, released_col)
                                        move = Move(initial, final)

                                        # check valid move
                                        if board.valid_move(dragger.piece, move):
                                            board.move(dragger.piece, move)
                                            # draw piece on board
                                            game.show_bg(screen)
                                            game.show_last_move(screen)
                                            game.show_pieces(screen)
                                            # next turn
                                            board.addMove(piece, released_col, released_row, dragger.initial_col, self.ai_starting, self.chessBoard)
                                            if (board.checkmate(self.chessBoard)):
                                                if (piece.color == "white"):
                                                    self.winnerColor = "White"
                                                else:
                                                    self.winnerColor = "Black"
                                                self.winner = "True"
                                                self.gameover = True          
                                            game.next_turn(self.ai_starting)
                                            print("Game Score: ", board.heuristic())
                                            self.ai_move = True
                                        
                                        dragger.undrag_piece()

                                    # board.generate_moves_ai()

                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_r:
                                game.reset()
                                game = self.game
                                board = self.game.board
                                dragger = self.game.dragger
                                self.gameover = False
                                self.winner = ""

                            if event.key == pygame.K_q:
                                self.starting = True
                                game.reset()
                                game = self.game
                                board = self.game.board
                                dragger = self.game.dragger
                                self.gameover = False
                                self.winner = ""

                # quit app
                if (event.type == pygame.QUIT):
                    pygame.quit()
                    sys.exit()

            pygame_widgets.update(pygame.event.get())
            pygame.display.update()


main = Main()
main.mainloop()
