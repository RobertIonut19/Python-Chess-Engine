"""
This program handles user input and displays a chess game using Pygame.

Constants:
    WIDTH (int): The width of the chessboard display window.
    HEIGHT (int): The height of the chessboard display window.
    DIMENSION (int): The size of the chessboard (8x8).
    SQ_SIZE (int): The size of each square on the chessboard.
    MAX_FPS (int): The maximum frames per second for the display.
    IMAGES (dict): A dictionary containing images for different chess pieces.

Functions:
    load_images():
        Initializes a global dictionary of images for chess pieces.

    main():
        The main function that initializes Pygame, sets up the display window,
        and handles user input and graphics updates.

Usage:
    - Run this script to start the chess game.
"""
import sys
from Chess_Project.Chess import ChessEngine
import pygame as p

WIDTH = 512  # width of the chessboard display window
HEIGHT = 512  # height of the chessboard display window
DIMENSION = 8  # size of the chessboard (8x8)

SQ_SIZE = HEIGHT // DIMENSION  # size of each square on the chessboard

MAX_FPS = 15  # maximum frames per second for the display
IMAGES = {}


def load_images():
    """
    Initializes a global dictionary of images for chess pieces.
    This function loads and scales images for each chess piece and stores them in the IMAGES dictionary.
    """
    pieces = ["wp", "wR", "wN", "wB", "wK", "wQ", "bp", "bR", "bN", "bB", "bK", "bQ"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


def main():
    """
    The main function that initializes Pygame, sets up the display window, and handles user input and graphics updates.

    This function initializes Pygame, sets up the display window, creates a GameState object, and prints the initial chessboard state.
    """
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))

    game_state = ChessEngine.GameState()
    valid_moves = game_state.getValidMoves()
    move_made = False  # flag variable for when a move is made
    load_images()

    animate = False

    squareSelected = ()  # a tuple to store the coordinates of pieces selected
    # keeps track of the last click on the table (row ,col)
    playerClicks = []  # keeps track of playerClicks  (example [(6,1), (4, 1)] )

    font = p.font.Font(None, 36)
    turn_text = font.render("Turn: White", True, p.Color("black"))

    game_over = False

    running = True
    while running:
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
            # mouse handler
            elif event.type == p.MOUSEBUTTONDOWN:
                if not game_over:
                    location = p.mouse.get_pos()  # (location[0] // SQ_SIZE, location[1] // SQ_SIZE)
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE

                    if squareSelected == (row, col):  # unselect a piece
                        playerClicks = [(row, col)]
                    else:
                        squareSelected = (row, col)
                        playerClicks.append(squareSelected)  # it will store both clicks
                        if (len(playerClicks) == 0):
                            if (game_state.whiteToMove and game_state.board[row][col][0] != 'w') or (
                                    not game_state.whiteToMove and game_state.board[row][col][0] != 'b'):
                                playerClicks = []
                                squareSelected = ()
                        elif (len(playerClicks) == 2):
                            if (game_state.whiteToMove and game_state.board[row][col][0] == 'w') or (
                                    not game_state.whiteToMove and game_state.board[row][col][0] == 'b'):
                                playerClicks = [(row, col)]
                                squareSelected = (row, col)
                    if len(playerClicks) == 2:
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], game_state.board)
                        # print(move.get_chess_notation())
                        for i in range(len(valid_moves)):
                            if move == valid_moves[i]:
                                game_state.makeMove(valid_moves[i])
                                move_made = True
                                animate = True
                                squareSelected = ()  # reset the user clicks
                                playerClicks = []
                        if not move_made:
                            playerClicks = [squareSelected]
            # key handler
            elif event.type == p.KEYDOWN:

                if event.key == p.K_z:  # undo when 'z' is pressed
                    game_state.undoMove()
                    move_made = True
                    animate = False
                if event.key == p.K_r:  # reset the board when 'r' is pressed
                    game_state = ChessEngine.GameState()
                    valid_moves = game_state.getValidMoves()
                    squareSelected = ()
                    playerClicks = []
                    move_made = False
                    animate = False


        if move_made:
            if animate:
                animate_move(game_state.moveLog[-1], screen, game_state.board, clock)
            valid_moves = game_state.getValidMoves()
            move_made = False
            animate = False

        if game_state.check_mate:
            game_over = True
            if game_state.whiteToMove:
                draw_end_game(screen, "Black wins by checkmate")
            else:
                draw_end_game(screen, "White wins by checkmate")

        clock.tick(MAX_FPS)
        p.display.flip()
        drawGameState(screen, game_state, squareSelected)

def highlight_squares(screen, game_state, valid_moves, squareSelected):
    '''
    Highlight square selected and moves for piece selected
    '''
    if squareSelected != ():
        r, c = squareSelected
        if game_state.board[r][c][0] == ('w' if game_state.whiteToMove else 'b'):  # square selected is a piece that can be moved
            # highlight selected square
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)  # transparency value -> 0 transparent; 255 opaque
            s.fill(p.Color('green'))
            screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))
            # highlight moves from that square
            s.fill(p.Color('yellow'))
            for move in valid_moves:
                if move.start_row == r and move.start_col == c:
                    screen.blit(s, (move.end_col * SQ_SIZE, move.end_row * SQ_SIZE))

def drawGameState(screen, gs,  squareSelected):
    """
    This function will be responsible for all the graphics within a current game state.
    """
    drawBoard(screen)  # draw squares on the board

    highlight_squares(screen, gs, gs.getValidMoves(), squareSelected)

    drawPieces(screen, gs.board)  # draw pieces on top of those squares

    drawNotation(screen)


def drawNotation(screen):
    """
    This function will draw the chess notation on the side.
    """
    font = p.font.Font(None, 24)
    for i in range(DIMENSION):
        notation_text = font.render(str(DIMENSION - i), True, p.Color("black"))
        screen.blit(notation_text, (WIDTH + 5, i * SQ_SIZE + 5))  # Display row notation

    for i in range(DIMENSION):
        notation_text = font.render(chr(ord('a') + i), True, p.Color("black"))
        screen.blit(notation_text, (WIDTH + i * SQ_SIZE + 5, HEIGHT - 25))  # Display column notation


def drawBoard(screen):
    """
    This function will draw the squares on the board.
    """
    global colors
    colors = [p.Color("white"), p.Color("grey")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]  # all the even squares will be white, all the odd squares will be green
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawPieces(screen, board):
    """
    This function will draw the pieces on the board using the current GameState.board.
    """
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def animate_move(move, screen, board, clock):
    '''
    This function will animate a move
    '''
    global colors
    dR = move.end_row - move.start_row
    dC = move.end_col - move.start_col
    frames_per_square = 5 # frames to move one square
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

def draw_end_game(screen, text):
    '''
    This function will draw the end game screen
    '''
    font = p.font.Font(None, 32)
    text_object = font.render(text, 0, p.Color('Grey'))
    text_location = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH / 2 - text_object.get_width() / 2,
                                                     HEIGHT / 2 - text_object.get_height() / 2)
    screen.blit(text_object, text_location)
    text_object = font.render(text, 0, p.Color('Black'))
    screen.blit(text_object, text_location.move(2, 2))

if __name__ == "__main__":
    main()
