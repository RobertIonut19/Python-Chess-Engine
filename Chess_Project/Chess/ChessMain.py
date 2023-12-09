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
    load_images()

    running = True
    while running:
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
                p.quit()
                sys.exit()
        clock.tick(MAX_FPS)
        p.display.flip()
        drawGameState(screen, game_state)


def drawGameState(screen, gs):
    """
    This function will be responsible for all the graphics within a current game state.
    """
    drawBoard(screen) #draw squares on the board

    drawPieces(screen, gs.board) #draw pieces on top of those squares


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
