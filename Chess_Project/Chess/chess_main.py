"""
This program handles user input and displays a chess game using Pygame.

Constants:
    B_WIDTH (int): The WIDTH of the chessboard display window.
    B_HEIGHT (int): The height of the chessboard display window.
    DIMENSION (int): The size of the chessboard (8x8).
    SQ_SIZE (int): The size of each square on the chessboard.
    MAX_FPS (int): The maximum frames per second for the display.
    IMAGES (dict): A dictionary containing images for different chess pieces.

Functions:
    load_images():
        Initializes a global dictionary of images for chess pieces.

    Button:
        A class representing a clickable button.

        Methods:
            __init__(self, text, x, y, width, height, color, hover_color, action):
                Initializes a Button instance.

            draw(self, screen, font):
                Draws the button on the screen.

            check_click(self, event):
                Checks if the button is clicked and performs the associated action.

    quit_game():
        Quits the game and exits the program.

    start_game():
        Sets the game state to "game" and exits the menu.

    set_player_one():
        Sets the player_one variable to True.

    set_player_two():
        Sets the player_two variable to True.

    main():
        The main function that initializes Pygame, sets up the display window,
        and handles user input and graphics updates.

Usage:
    - Run this script to start the chess game.
"""
import sys
from Chess_Project.Chess import chess_engine, random_move
import pygame as p

B_WIDTH = 600  # width of the chessboard display window
B_HEIGHT = 600  # height of the chessboard display window
DIMENSION = 8  # size of the chessboard (8x8)
LEFT_PANEL_WIDTH = 200
LEFT_PANEL_HEIGTH = B_HEIGHT

SQ_SIZE = B_HEIGHT // DIMENSION  # size of each square on the chessboard

MAX_FPS = 60  # maximum frames per second for the display
IMAGES = {}

WHITE = (162,213,198)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

BUTTON_WIDTH, BUTTON_HEIGHT = 200, 50
BUTTON_MARGIN = 20
FONT_SIZE = 36

player_one = False
player_two = False

game_state = "menu"
running = False
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

def quit_game():
    """
        Quits the game and exits the program.

        Returns:
            None
    """
    p.quit()
    sys.exit()

def start_game():
    """
        Sets the game state to "game" and exits the menu.

        Returns:
            None
    """
    global game_state, running
    print("Starting game...")
    game_state = "game"
    print("Game started")
    running = False

def set_player_one():
    """
        Sets the player_one variable to True.

        Returns:
            None
    """
    global player_one
    player_one = True
    print("Player One selected")

def set_player_two():
    """
       Sets the player_two variable to True.

       Returns:
           None
    """
    global player_two
    player_two = True
    print("Player Two selected")


player_one_button = Button("White - Person", B_WIDTH // 2 - BUTTON_WIDTH // 2, B_HEIGHT // 2 - BUTTON_HEIGHT - BUTTON_MARGIN, BUTTON_WIDTH, BUTTON_HEIGHT, p.Color(7,123,138), p.Color(92,60,146), set_player_one)
player_two_button = Button("Black - Person", B_WIDTH // 2 - BUTTON_WIDTH // 2, B_HEIGHT // 2, BUTTON_WIDTH, BUTTON_HEIGHT, p.Color(7,123,138), p.Color(92,60,146), set_player_two)
play_button = Button("Play", B_WIDTH // 2 - BUTTON_WIDTH // 2, B_HEIGHT // 2 + BUTTON_HEIGHT + BUTTON_MARGIN, BUTTON_WIDTH, BUTTON_HEIGHT, p.Color(7,123,138), p.Color(92,60,146), start_game)
quit_button = Button("Quit", B_WIDTH // 2 - BUTTON_WIDTH // 2, B_HEIGHT // 2 + 3 * (BUTTON_HEIGHT + BUTTON_MARGIN), BUTTON_WIDTH, BUTTON_HEIGHT, p.Color(215,38,49), p.Color(92,60,146), quit_game)

buttons = [player_one_button, player_two_button, play_button, quit_button]


def load_images():
    """
    Initializes a global dictionary of images for chess pieces.
    This function loads and scales images for each chess piece and stores them in the IMAGES dictionary.
    """
    pieces = ["wp", "wR", "wN", "wB", "wK", "wQ", "bp", "bR", "bN", "bB", "bK", "bQ"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE-10, SQ_SIZE-10))


def main():
    """
    The main function that initializes Pygame, sets up the display window, and handles user input and graphics updates.

    This function initializes Pygame, sets up the display window, creates a GameState object, and prints the initial
    chessboard state.
    """
    global game_state, running
    p.init()
    screen = p.display.set_mode((B_WIDTH, B_HEIGHT))
    p.display.set_caption("Chess")
    clock = p.time.Clock()

    game_state= "menu"

    running = True
    while running:
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False

            for button in buttons:
                button.check_click(event)

        screen.fill(WHITE)

        if game_state == "menu":
            for button in buttons:
                button.draw(screen, p.font.Font(None, FONT_SIZE))
        elif game_state == "game":
            # Transition to game
            print("Transitioning to game state...")
            running = False

        p.display.flip()
        clock.tick(MAX_FPS)

    screen = p.display.set_mode((B_WIDTH + LEFT_PANEL_WIDTH, B_HEIGHT + 25))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))

    game_state = chess_engine.GameState()
    valid_moves = game_state.get_valid_moves()
    move_made = False  # flag variable for when a move is made
    load_images()

    animate = False

    square_selected = ()  # a tuple to store the coordinates of pieces selected
    # keeps track of the last click on the table (row ,col)
    player_clicks = []  # keeps track of player_clicks  (example [(6,1), (4, 1)] )

    game_over = False

    running = True
    while running:
        human_turn = (game_state.white_to_move and player_one) or (not game_state.white_to_move and player_two)
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
            # mouse handler
            elif event.type == p.MOUSEBUTTONDOWN:
                if not game_over and human_turn:
                    location = p.mouse.get_pos()  # (location[0] // SQ_SIZE, location[1] // SQ_SIZE)
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE

                    if square_selected == (row, col) or col >= 8:  # unselect a piece
                        player_clicks = [(row, col)]
                    else:
                        square_selected = (row, col)
                        player_clicks.append(square_selected)  # it will store both clicks
                        if (len(player_clicks) == 0):
                            if (game_state.white_to_move and game_state.board[row][col][0] != 'w') or (
                                    not game_state.white_to_move and game_state.board[row][col][0] != 'b'):
                                player_clicks = []
                                square_selected = ()
                        elif (len(player_clicks) == 2):
                            if (game_state.white_to_move and game_state.board[row][col][0] == 'w') or (
                                    not game_state.white_to_move and game_state.board[row][col][0] == 'b'):
                                player_clicks = [(row, col)]
                                square_selected = (row, col)
                    if len(player_clicks) == 2:
                        move = chess_engine.Move(player_clicks[0], player_clicks[1], game_state.board)
                        print(move.get_chess_notation())
                        for i in range(len(valid_moves)):
                            if move == valid_moves[i]:
                                game_state.make_move(valid_moves[i])
                                move_made = True
                                animate = True
                                square_selected = ()  # reset the user clicks
                                player_clicks = []
                        if not move_made:
                            player_clicks = [square_selected]

                if not game_over and not human_turn:
                    move = random_move.random_move(valid_moves)
                    game_state.make_move(move)
                    game_state.move_log.append(move)
                    move_made = True
                    animate = True

            # key handler
            elif event.type == p.KEYDOWN:

                if event.key == p.K_z:  # undo when 'z' is pressed
                    game_state.undo_move()
                    move_made = True
                    animate = False
                if event.key == p.K_r:  # reset the board when 'r' is pressed
                    game_state = chess_engine.GameState()
                    valid_moves = game_state.get_valid_moves()
                    square_selected = ()
                    player_clicks = []
                    move_made = False
                    animate = False


        if move_made:
            if animate:
                animate_move(game_state.move_log[-1], screen, game_state.board, clock)
            valid_moves = game_state.get_valid_moves()
            move_made = False
            animate = False

        if game_state.check_mate:
            game_over = True
            if game_state.white_to_move:
                draw_end_game(screen, "Black wins by checkmate")
            else:
                draw_end_game(screen, "White wins by checkmate")
        elif game_state.stale_mate:
            game_over = True
            draw_end_game(screen, "Stalemate")

        clock.tick(MAX_FPS)
        p.display.flip()
        draw_game_state(screen, game_state, square_selected)

def highlight_squares(screen, game_state, valid_moves, square_selected):
    """
    Highlight square selected and moves for the selected piece.

    Parameters:
    - screen (pygame.display): The game screen.
    - game_state (ChessGameState): The current state of the chess game.
    - valid_moves (list): List of valid moves for the selected piece.
    - square_selected (tuple): Tuple containing the (row, column) of the selected square.

    Returns:
    None
    """
    if square_selected != ():
        r, c = square_selected
        if game_state.board[r][c][0] == ('w' if game_state.white_to_move else 'b'):  # square selected is a piece that can be moved
            # highlight selected square
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)  # transparency value -> 0 transparent; 255 opaque
            s.fill(p.Color(253,185,201))
            screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))
            # highlight moves from that square
            s.fill(p.Color(187,246,243))
            for move in valid_moves:
                if move.start_row == r and move.start_col == c:
                    screen.blit(s, (move.end_col * SQ_SIZE, move.end_row * SQ_SIZE))

def draw_game_state(screen, gs, square_selected):
    """
    Draw all the graphics within a current game state.

    Parameters:
    - screen (pygame.Surface): The game screen.
    - gs (GameState): The current game state.
    - square_selected (tuple): The selected square coordinates.

    Returns:
    None
    """
    drawBoard(screen)  # draw squares on the board

    highlight_squares(screen, gs, gs.get_valid_moves(), square_selected)

    drawPieces(screen, gs.board)  # draw pieces on top of those squares

    drawNotation(screen)

    draw_move_log(screen, gs)
def drawNotation(screen):
    """
    Draw chess notation on the side of the chessboard.

    Parameters:
    - screen (pygame.Surface): The game screen.

    Returns:
    None
    """
    font = p.font.Font(None, 24)
    for i in range(DIMENSION):
        notation_text = font.render(str(DIMENSION - i), True, p.Color("black"))
        screen.blit(notation_text, (B_WIDTH + 5, i * SQ_SIZE + 25))  # Display row notation

    for i in range(DIMENSION):
        notation_text = font.render(chr(ord('a') + i), True, p.Color("black"))
        screen.blit(notation_text, (25 +  i * SQ_SIZE + 5, B_HEIGHT + 5))  # Display column notation

    line = p.Rect(B_WIDTH, 0, 3, B_HEIGHT)
    p.draw.rect(screen, p.Color("black"), line)
    line = p.Rect(0, B_HEIGHT, B_WIDTH+3, 3)
    p.draw.rect(screen, p.Color("black"), line)


def drawBoard(screen):
    """
    Draw the chessboard squares on the screen.

    Parameters:
    - screen (pygame.Surface): The game screen.

    Returns:
    None
    """
    global colors
    colors = [p.Color(227, 193, 111), p.Color(184, 139, 74)]

    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]  # Alternating colors for chessboard squares
            rect = p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            p.draw.rect(screen, color, rect)
import pygame as p

def drawPieces(screen, board):
    """
    Draw the chess pieces on the board using the current game state.

    Parameters:
    - screen (pygame.Surface): The game screen.
    - board (list): The 2D list representing the chessboard.

    Returns:
    None
    """
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                # Draw the piece on the screen at the appropriate position
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE + 5, r * SQ_SIZE + 5, SQ_SIZE, SQ_SIZE))

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
    global colors
    dR = move.end_row - move.start_row
    dC = move.end_col - move.start_col
    frames_per_square = 5  # frames to move one square
    frame_count = (abs(dR) + abs(dC)) * frames_per_square
    for frame in range(frame_count + 1):
        r, c = (move.start_row + (dR) * frame / frame_count, move.start_col + dC * frame / frame_count)
        drawBoard(screen)
        drawPieces(screen, board)
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

def draw_move_log(screen, gs):
    """
    Draw the move log on the game screen.

    Parameters:
    - screen (pygame.Surface): The game screen.
    - gs (GameState): The current game state.

    Returns:
    None
    """
    left_panel = p.Rect(B_WIDTH + 20, 0, LEFT_PANEL_WIDTH, LEFT_PANEL_HEIGTH + 25)
    p.draw.rect(screen, p.Color('black'), left_panel)
    move_log = gs.move_log
    font = p.font.Font(None, 20)
    text_color = p.Color('white')
    text_y = 5
    cond = 0
    first = 0

    for i in range(0, len(move_log), 2):
        text = move_log[i].get_chess_notation()
        text_object = font.render(text, True, text_color)
        text_location = left_panel.move(5 + cond, text_y)
        if text_location.top > B_HEIGHT:
            if first == 0:
                cond = 50
                text_location = left_panel.move(5 + cond, 5)
                text_y = 5
                first = 1
        if text_location.top > B_HEIGHT:
            if first == 1:
                cond = 100
                text_location = left_panel.move(5 + cond, 5)
                text_y = 5
                first = 2

        screen.blit(text_object, text_location)
        text_y += text_object.get_height()

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

if __name__ == "__main__":
    main()
