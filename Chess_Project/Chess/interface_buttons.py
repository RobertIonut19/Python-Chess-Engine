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

WHITE = (162,213,198)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

BUTTON_WIDTH, BUTTON_HEIGHT = 200, 50
BUTTON_MARGIN = 20

class Button:
    def __init__(self, x, y, image, action):
        """
            Initializes a Button instance.

            Args:
                image (pygame.Surface): The image of the button.
                x (int): The x-coordinate of the button.
                y (int): The y-coordinate of the button.
                action (function): The function to be executed when the button is clicked.
            """
        self.action = action
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.is_clicked = False

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
