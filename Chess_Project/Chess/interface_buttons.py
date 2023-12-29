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

class Button:
    def __init__(self, text, x, y, width, height, color, hover_color, action):
        """
            Initializes a Button instance.

            Args:
                text (str): The text displayed on the button.
                x (int): The x-coordinate of the button.
                y (int): The y-coordinate of the button.
                width (int): The width of the button.
                height (int): The height of the button.
                color (tuple): The color of the button.
                hover_color (tuple): The color of the button when hovered.
                action (function): The function to be executed when the button is clicked.
            """
        self.rect = p.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.text = text
        self.action = action

    def draw(self, screen, font):
        """
            Draws the button on the screen.

            Args:
                screen (pygame.Surface): The game screen.
                font (pygame.font.Font): The font used for the button text.

            Returns:
                None
        """
        p.draw.rect(screen, self.hover_color if self.rect.collidepoint(p.mouse.get_pos()) else self.color, self.rect)
        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

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
