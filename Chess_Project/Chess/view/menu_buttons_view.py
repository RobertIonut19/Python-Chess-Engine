"""
Button class for the Chess game:
        A class representing a clickable button.

        Methods:
            __init__(self, text, x, y, width, height, color, hover_color, action):
                Initializes a Button instance.

            draw(self, screen, font):
                Draws the button on the screen.

            check_click(self, event):
                Checks if the button is clicked and performs the associated action.
"""

import pygame as p
import numpy as np
import sys

WHITE = (162,213,198)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

BUTTON_WIDTH, BUTTON_HEIGHT = 200, 50
BUTTON_MARGIN = 20

B_WIDTH = 600  # width of the chessboard display window
B_HEIGHT = 600  # height of the chessboard display window

MENU_IMAGES = []
BUTTONS = []

class Button:
    def __init__(self, screen, x, y, image, action):
        """
            Initializes a Button instance.

            Args:
                image (pygame.Surface): The image of the button.
                x (int): The x-coordinate of the button.
                y (int): The y-coordinate of the button.
                action (function): The function to be executed when the button is clicked.
            """
        self.screen = screen
        self.action = action
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.is_clicked = False
        self.hovered = False
        self.i = 0

    def draw(self, screen, font):
        """
            Draws the button on the screen.

            Args:
                screen (pygame.Surface): The game screen.
                font (pygame.font.Font): The font used for the button text.

            Returns:
                None
        """
        scaled_image = p.transform.scale(self.image, (BUTTON_WIDTH, BUTTON_HEIGHT))

        x_offset = (BUTTON_WIDTH - scaled_image.get_width()) // 2
        y_offset = (BUTTON_HEIGHT - scaled_image.get_height()) // 2

        screen.blit(self.image, (self.rect.x + x_offset, self.rect.y + y_offset))

    def check_click(self, event):
        """
        Checks if the button is clicked and performs
        the associated action.

        Args:
            event(pygame.event.Event): The pygame event.

        Returns:
            None
        """
        if event.type == p.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.action()
                self.is_clicked = not self.is_clicked
                if self.is_clicked:
                    self.image.set_alpha(150)
                else:
                    self.image.set_alpha(255)

        if event.type == p.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                for self.i in range(4):
                    if MENU_IMAGES[self.i] == self.image:
                        self.image = MENU_IMAGES[self.i + 5]
                        self.hovered = True
                        print("hover")
                        break
            else:
                print(self.i, self.hovered)
                for self.i in range(10):
                    if MENU_IMAGES[self.i] == self.image and self.hovered == True:
                        self.image = MENU_IMAGES[self.i - 5]
                        if self.is_clicked:
                            self.image.set_alpha(150)
                        else:
                            self.image.set_alpha(255)
                        self.hovered = False
                        print("not hover")
                        break

def load_images():
    # Menu
    global MENU_IMAGES
    ai_white = p.transform.scale(p.image.load("view/images/menu/ai_white.png"), (BUTTON_WIDTH, BUTTON_HEIGHT))
    ai_black = p.transform.scale(p.image.load("view/images/menu/ai_black.png"), (BUTTON_WIDTH, BUTTON_HEIGHT))
    play_button = p.transform.scale(p.image.load("view/images/menu/play_button.png"),
                                    (BUTTON_WIDTH, BUTTON_HEIGHT))
    quit_button = p.transform.scale(p.image.load("view/images/menu/quit_button.png"),
                                    (BUTTON_WIDTH, BUTTON_HEIGHT))
    menu_background = p.transform.scale(p.image.load("view/images/menu/menu.png"), (B_WIDTH, B_HEIGHT))

    MENU_IMAGES.append(ai_white); MENU_IMAGES.append(ai_black)
    MENU_IMAGES.append(play_button); MENU_IMAGES.append(quit_button)
    MENU_IMAGES.append(menu_background)

    ai_white_hover = p.transform.scale(p.image.load("view/images/menu/ai_white_hover.png"), (BUTTON_WIDTH, BUTTON_HEIGHT))
    ai_black_hover = p.transform.scale(p.image.load("view/images/menu/ai_black_hover.png"), (BUTTON_WIDTH, BUTTON_HEIGHT))
    play_button_hover = p.transform.scale(p.image.load("view/images/menu/play_hover.png"),
                                    (BUTTON_WIDTH, BUTTON_HEIGHT))
    quit_button_hover = p.transform.scale(p.image.load("view/images/menu/quit_hover.png"),
                                    (BUTTON_WIDTH, BUTTON_HEIGHT))

    MENU_IMAGES.append(ai_white_hover); MENU_IMAGES.append(ai_black_hover)
    MENU_IMAGES.append(play_button_hover); MENU_IMAGES.append(quit_button_hover)

