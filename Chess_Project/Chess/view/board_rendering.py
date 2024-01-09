import pygame as p

B_WIDTH = 600  # width of the chessboard display window
B_HEIGHT = 600  # height of the chessboard display window
DIMENSION = 8  # size of the chessboard (8x8)
LEFT_PANEL_WIDTH = 200
LEFT_PANEL_HEIGHT = B_HEIGHT

SQ_SIZE = B_HEIGHT // DIMENSION  # size of each square on the chessboard

MAX_FPS = 60  # maximum frames per second for the display
IMAGES = {}


def load_images():
    """
    Initializes a global dictionary of images for chess pieces.
    This function loads and scales images for each chess piece and stores them in the IMAGES dictionary.
    """
    # Board pieces
    pieces = ["wp", "wR", "wN", "wB", "wK", "wQ", "bp", "bR", "bN", "bB", "bK", "bQ"]
    path = "view/images/pieces/"

    for piece in pieces:
        if piece[1] == 'p':
            IMAGES[piece] = p.transform.scale(p.image.load(path + piece + ".png"), (SQ_SIZE - 14, SQ_SIZE - 14))
        else:
            IMAGES[piece] = p.transform.scale(p.image.load(path + piece + ".png"), (SQ_SIZE - 10, SQ_SIZE - 10))


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
    draw_board(screen)  # draw squares on the board

    highlight_squares(screen, gs, gs.get_valid_moves(), square_selected)

    draw_pieces(screen, gs.board)  # draw pieces on top of those squares

    draw_notation(screen)

    draw_move_log(screen, gs)


def draw_board(screen):
    """
    Draw the chessboard squares on the screen.

    Parameters:
    - screen (pygame.Surface): The game screen.

    Returns:
    None
    """
    
    colors = [p.Color(227, 193, 111), p.Color(184, 139, 74)]

    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]  # Alternating colors for chessboard squares
            rect = p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            p.draw.rect(screen, color, rect)


def draw_pieces(screen, board):
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
        if game_state.board[r][c][0] == ('w' if game_state.white_to_move else 'b'):  
            # square selected is a piece that can be moved
            # highlight selected square
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)  # transparency value -> 0 transparent; 255 opaque
            s.fill(p.Color(253, 185, 201))
            screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))
            # highlight moves from that square
            s.fill(p.Color(187, 246, 243))
            for move in valid_moves:
                if move.start_row == r and move.start_col == c:
                    screen.blit(s, (move.end_col * SQ_SIZE, move.end_row * SQ_SIZE))


def draw_notation(screen):
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
        screen.blit(notation_text, (25 + i * SQ_SIZE + 5, B_HEIGHT + 5))  # Display column notation

    line = p.Rect(B_WIDTH, 0, 3, B_HEIGHT)
    p.draw.rect(screen, p.Color("black"), line)
    line = p.Rect(0, B_HEIGHT, B_WIDTH+3, 3)
    p.draw.rect(screen, p.Color("black"), line)


def draw_move_log(screen, gs):
    """
    Draw the move log on the game screen.

    Parameters:
    - screen (pygame.Surface): The game screen.
    - gs (GameState): The current game state.

    Returns:
    None
    """
    left_panel = p.Rect(B_WIDTH + 20, 0, LEFT_PANEL_WIDTH, LEFT_PANEL_HEIGHT + 25)
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
