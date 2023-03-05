import pygame
from const import *
import pygame_widgets
from pygame_widgets.button import Button
from pygame_widgets.textbox import TextBox

class Start:

    def __init__(self):
        self.background = (49, 46, 43)

    def starting_screen(self, screen):

        # self.button(screen, 250, 70, "Play with Player", (127, 166,
        #             80), (149, 187, 74), starting, btn_seperator=0)
        # self.button(screen, 250, 70, "Play with AI",
        #             (56, 54, 52), (74, 72, 70), starting)

        screen.fill(self.background)
        self.text(screen)


    def button(self, screen, btn_width, btn_height, text, color1, color2, starting, btn_seperator=90):
        button = Button(
            # Mandatory Parameters
            screen,
            (WIDTH - btn_width) // 2,
            (HEIGHT - btn_height) // 2 + btn_seperator,
            btn_width,
            btn_height,

            # Optional Parameters
            text=text,
            textColour=(255, 255, 255),
            fontSize=40,
            margin=5,
            inactiveColour=color1,
            hoverColour=color2,
            pressedColour=color2,
            radius=20,
            onClick=lambda: self.start(starting)
        )

    def text(self, screen):
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('Play Chess Online or with AI',
                           True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = (WIDTH // 2, (HEIGHT // 2) - 100)

        screen.blit(text, textRect)
