import pygame as p

from .board_rendering import *
from Chess_Project.Chess.view import menu_buttons_view as menu

B_WIDTH = 600  # width of the chessboard display window
B_HEIGHT = 600  # height of the chessboard display window
DIMENSION = 8  # size of the chessboard (8x8)
LEFT_PANEL_WIDTH = 200

SQ_SIZE = B_HEIGHT // DIMENSION  # size of each square on the chessboard

MAX_FPS = 60  # maximum frames per second for the display

FONT_SIZE = 32


class ChessView:
    """
    Class representing the view for the Chess game.

    Attributes:
        - screen (pygame.Surface): The game screen.
        - clock (pygame.time.Clock): The game clock.
        - game_situation (str): The current situation of the game (e.g., "menu" or "game").
        - white_player (bool): Flag indicating whether the white player is controlled by AI.
        - black_player (bool): Flag indicating whether the black player is controlled by AI.
        - running (bool): Flag indicating whether the game is currently running.

    Methods:
        - __init__(self): Initializes the ChessView object.
        - draw(self, game_state, square_selected=(), game_situation="game"): Draws the game state.
        - create_buttons(self, screen): Creates buttons for the menu.
        - draw_menu(self): Draws the menu screen.
        - start_game(self): Initiates the chess game.
        - set_ai_white(self): Toggles AI control for the white player.
        - set_ai_black(self): Toggles AI control for the black player.
        - quit_game(self): Quits the game.
        - draw_board(self, game_state, square_selected=()): Draws the chessboard.
        - animate_move(self, move, screen, board, clock): Animates a chess move on the screen.
        - game_initialization(self): Initializes the game.

    """
    def __init__(self):
        """
        Initialize the ChessView object.
        This method initializes the game screen, clock, and other attributes for the ChessView.
        Parameters:
            self (ChessView): The ChessView object to be initialized.
        Returns:
            None
        """
        p.init()
        self.screen = p.display.set_mode((B_WIDTH, B_HEIGHT))
        self.screen.fill(p.Color("white"))
        p.display.set_caption("Chess")
        load_images()
        self.clock = p.time.Clock()

        menu.load_images()
        self.game_situation = "menu"
        self.white_player = True
        self.black_player = True
        self.running = True

        self.create_buttons(self.screen)

    def draw(self, game_state, square_selected=(), game_situation="game"):
        """
            Draw the game state on the screen.

            Parameters:
                - game_state: The current state of the chess game.
                - square_selected (tuple): The selected square coordinates.
                - game_situation (str): The current situation of the game.

            Returns:
                None
        """
        if game_situation == "menu":
            self.draw_menu()
        elif game_situation == "game":
            self.draw_board(game_state, square_selected)

    def create_buttons(self, screen):
        """
            Create buttons for the menu.

            Parameters:
                - screen (pygame.Surface): The game screen.

            Returns:
                None
        """
        player_one_button = menu.Button(screen, B_WIDTH // 2 - menu.BUTTON_WIDTH // 2,
                                        B_HEIGHT // 2 - 35 - menu.BUTTON_HEIGHT - menu.BUTTON_MARGIN,
                                        menu.MENU_IMAGES[0], self.set_ai_white)
        player_two_button = menu.Button(screen, B_WIDTH // 2 - menu.BUTTON_WIDTH // 2, B_HEIGHT // 2 - 35,
                                        menu.MENU_IMAGES[1], self.set_ai_black)
        play_button = menu.Button(screen, B_WIDTH // 2 - menu.BUTTON_WIDTH // 2,
                                  B_HEIGHT // 2 - 35 + menu.BUTTON_HEIGHT + menu.BUTTON_MARGIN,
                                  menu.MENU_IMAGES[2], self.start_game)
        quit_button = menu.Button(screen, B_WIDTH // 2 - menu.BUTTON_WIDTH // 2,
                                  B_HEIGHT // 2 + 3 * (menu.BUTTON_HEIGHT + menu.BUTTON_MARGIN),
                                  menu.MENU_IMAGES[3], self.quit_game)

        menu.BUTTONS = [player_one_button, player_two_button, play_button, quit_button]

    def draw_menu(self):
        """
            Draw the menu screen.

            Parameters:
                None

            Returns:
                None
        """
        self.screen.blit(menu.MENU_IMAGES[4], (0, 0))
        for button in menu.BUTTONS:
            button.draw(self.screen)

    def start_game(self):
        """
            Start the chess game.

            Parameters:
                None

            Returns:
                None
        """
        self.game_situation = "game"

        print("start game")

    def set_ai_white(self):
        """
            Toggle AI control for the white player.

            Parameters:
                None

            Returns:
                None
        """
        self.white_player = not self.white_player
        print("set ai white")

    def set_ai_black(self):
        """
            Toggle AI control for the black player.

            Parameters:
                None

            Returns:
                None
        """
        self.black_player = not self.black_player
        print("set ai black")

    def quit_game(self):
        """
            Quit the game.

            Parameters:
                None

            Returns:
                None
        """
        self.running = False
        self.game_situation = "game"
        print("quit game")

    def draw_board(self, game_state, square_selected=()):
        """
        Draw the chessboard on the screen.

        Parameters:
            - game_state (ChessGameState): The current state of the chess game.
            - square_selected (tuple): The selected square coordinates.

        Returns:
            None
        """
        draw_game_state(self.screen, game_state, square_selected)

    @staticmethod
    def animate_move(move, screen, board, clock):
        """
        Animate a chess move on the screen.

        Parameters:
        - move (ChessMove): The move to animate.
        - screen (pygame.Surface): The game screen.
        - board (list): The 2D list representing the chessboard.
        - clock (pygame.time.Clock): The game clock.

        Returns:
        None
        """
        colors = [p.Color(227, 193, 111), p.Color(184, 139, 74)]
        dR = move.end_row - move.start_row
        dC = move.end_col - move.start_col
        frames_per_square = 5  # frames to move one square
        frame_count = (abs(dR) + abs(dC)) * frames_per_square
        for frame in range(frame_count + 1):
            r, c = (move.start_row + dR * frame / frame_count, move.start_col + dC * frame / frame_count)
            draw_board(screen)
            draw_pieces(screen, board)
            # erase the piece moved from its ending square
            color = colors[(move.end_row + move.end_col) % 2]
            end_square = p.Rect(move.end_col * SQ_SIZE, move.end_row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            p.draw.rect(screen, color, end_square)
            # draw captured piece onto rectangle
            if move.piece_captured != '--':
                screen.blit(IMAGES[move.piece_captured], end_square)
            # draw moving piece
            screen.blit(IMAGES[move.piece_moved], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            p.display.flip()
            clock.tick(60)

    def game_initialization(self):
        """
            Initialize the game screen to the proper dimensions.

            Parameters:
                None

            Returns:
                None
        """
        self.screen = p.display.set_mode((B_WIDTH + LEFT_PANEL_WIDTH, B_HEIGHT + 25))
        self.screen.fill(p.Color("white"))


def draw_end_game(screen, text):
    """
    Draw the end game screen with the specified text.

    Parameters:
    - screen (pygame.Surface): The game screen.
    - text (str): The text to be displayed on the end game screen.

    Returns:
    None
    """
    font = p.font.Font(None, 32)
    text_object = font.render(text, 0, p.Color('Gray'))
    text_location = p.Rect(0, 0, B_WIDTH, B_HEIGHT).move(B_WIDTH / 2 - text_object.get_width() / 2,
                                                         B_HEIGHT / 2 - text_object.get_height() / 2)
    screen.blit(text_object, text_location)
    text_object = font.render(text, 0, p.Color('Black'))
    screen.blit(text_object, text_location.move(2, 2))
