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
from Chess import ChessEngine
import pygame as p

WIDTH = 512  # width of the chessboard display window
HEIGHT = 512 # height of the chessboard display window
DIMENSION = 8 # size of the chessboard (8x8)

SQ_SIZE = HEIGHT // DIMENSION # size of each square on the chessboard

MAX_FPS = 15 # maximum frames per second for the display
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
    move_made = False #flag variable for when a move is made
    load_images()

    squareSelected = () # a tuple to store the coordinates of pieces selected
                        # keeps track of the last click on the table (row ,col)
    playerClicks = []   # keeps track of playerClicks  (example [(6,1), (4, 1)] )

    font = p.font.Font(None, 36)
    turn_text = font.render("Turn: White", True, p.Color("black"))

    running = True
    while running:
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
            #mouse handler
            elif event.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() # (location[0] // SQ_SIZE, location[1] // SQ_SIZE)
                col =  location[0]//SQ_SIZE
                row =  location[1]//SQ_SIZE

                if squareSelected == (row, col): #unselect a piece
                    playerClicks = [(row, col)]
                    print("Player clicks: ", playerClicks, ", " , "squareSelected: ", squareSelected, game_state.whiteToMove)
                else:
                    squareSelected = (row, col)
                    playerClicks.append(squareSelected) #it will store both clicks
                    print(len(playerClicks))
                    if (len(playerClicks) == 0):
                        if (game_state.whiteToMove and game_state.board[row][col][0] != 'w') or (not game_state.whiteToMove and game_state.board[row][col][0] != 'b'):
                            playerClicks = []
                            squareSelected = ()
                            print("Prima selectie", "Player clicks: ", playerClicks, ", ", "squareSelected: ", squareSelected, game_state.whiteToMove)
                    elif (len(playerClicks) == 2):
                        if (game_state.whiteToMove and game_state.board[row][col][0] == 'w') or (not game_state.whiteToMove and game_state.board[row][col][0] == 'b'):
                            playerClicks = [(row, col)]
                            squareSelected = (row, col)
                            print("A doua selectie", "Player clicks: ", playerClicks, ", " , "squareSelected: ", squareSelected, game_state.whiteToMove)
                    print("Player clicks: ", playerClicks, ", " , "squareSelected: ", squareSelected, game_state.whiteToMove)
                if len(playerClicks) == 2:
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], game_state.board)
                    #print(move.get_chess_notation())
                    if move in valid_moves:
                        game_state.makeMove(move)
                        move_made = True
                    squareSelected = () #reset the user clicks
                    playerClicks = []
            #key handler
            elif event.type == p.KEYDOWN:
                if event.key == p.K_z: #undo when 'z' is pressed
                    game_state.undoMove()
                    move_made = True

        if move_made:
            valid_moves = game_state.getValidMoves()
            move_made = False
            turn_text = font.render("Turn: " + ("White" if game_state.whiteToMove else "Black"), True, p.Color("black"))

        if move_made:
            valid_moves = game_state.getValidMoves()
            move_made = False

        clock.tick(MAX_FPS)
        p.display.flip()
        drawGameState(screen, game_state)


def drawGameState(screen, gs):
    """
    This function will be responsible for all the graphics within a current game state.
    """
    drawBoard(screen) #draw squares on the board

    drawPieces(screen, gs.board) #draw pieces on top of those squares

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
    colors = [p.Color("white"), p.Color("grey")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)] #all the even squares will be white, all the odd squares will be green
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
def drawPieces(screen, board):
    """
    This function will draw the pieces on the board using the current GameState.board.
    """
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

if __name__ == "__main__":
    main()
