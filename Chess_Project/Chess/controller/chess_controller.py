from Chess_Project.Chess.model import chess_model as model
from Chess_Project.Chess.view import chess_view as view
from Chess_Project.Chess.model.moves.move_class import Move
from Chess_Project.Chess.model.game_state_class import GameState
from Chess_Project.Chess.view import menu_buttons_view as menu
import pygame as p
import sys


class ChessController:
    """
        Controller class for the chess game, handling user input and managing the game flow.

        Attributes:
        - chess_model (ChessModel): An instance of the chess model.
        - chess_view (ChessView): An instance of the chess view.

        Methods:
        - handle_input(screen, event): Handles user input during the game.
        - handle_menu_input(event): Handles user input in the game menu.
        - game_initialization(white_player, black_player, game_situation, running): Initializes the game parameters.
        - end_game(screen): Displays the end game message based on the game state.
    """
    def __init__(self):
        """
        Initializes the ChessController by creating instances of ChessModel and ChessView.
        """
        self.chess_model = model.ChessModel()
        self.chess_model.valid_moves = self.chess_model.game_state.get_valid_moves()
        self.chess_view = view.ChessView()

    def handle_input(self, screen, event):
        """
        Handles user input during the chess game.

        Args:
            - screen: The Pygame screen surface.
            - event: The Pygame event to be handled.
        """
        # model part
        human_turn = (self.chess_model.game_state.white_to_move and self.chess_model.white_player) or (
                    not self.chess_model.game_state.white_to_move and self.chess_model.black_player)

        # Quit the game
        if event.type == p.QUIT:
            self.chess_model.running = False
        if event.type == p.KEYDOWN and event.key == p.K_ESCAPE:
            self.chess_model.running = False

        # Mouse event handlers
        elif event.type == p.MOUSEBUTTONDOWN:
            if not self.chess_model.game_over and human_turn:
                location = p.mouse.get_pos()
                col = location[0] // view.SQ_SIZE
                row = location[1] // view.SQ_SIZE
                if row < view.DIMENSION and col < view.DIMENSION:
                    if self.chess_model.square_selected == (row, col) or col >= view.DIMENSION or row >= view.DIMENSION:
                        self.chess_model.square_selected = ()
                        self.chess_model.player_clicks = []
                    else:
                        self.chess_model.square_selected = (row, col)
                        self.chess_model.player_clicks.append(self.chess_model.square_selected)

                    if len(self.chess_model.player_clicks) == 2:
                        move = Move(self.chess_model.player_clicks[0], self.chess_model.player_clicks[1],
                                    self.chess_model.game_state.board)
                        for i in range(len(self.chess_model.valid_moves)):
                            if move == self.chess_model.valid_moves[i]:
                                self.chess_model.game_state.make_move(self.chess_model.valid_moves[i])
                                print("move made", self.chess_model.valid_moves[i].get_chess_notation())
                                self.chess_model.game_state.move_log.append(self.chess_model.valid_moves[i])
                                self.chess_model.animate = True
                                self.chess_model.move_made = True
                                self.chess_model.square_selected = ()
                                self.chess_model.player_clicks = []

                        if not self.chess_model.move_made:
                            self.chess_model.player_clicks = [self.chess_model.square_selected]

            # AI move
            if not self.chess_model.game_over and not human_turn:
                move = self.chess_model.game_state.random_move(self.chess_model.valid_moves)
                self.chess_model.game_state.make_move(move)
                self.chess_model.game_state.move_log.append(move)
                self.chess_model.animate = True
                self.chess_model.move_made = True

        elif event.type == p.KEYDOWN:
            if event.key == p.K_z:
                self.chess_model.game_state.undo_move()
                if len(self.chess_model.game_state.move_log) != 0:
                    self.chess_model.game_state.move_log.pop()
                self.chess_model.animate = False
                self.chess_model.move_made = True
            if event.key == p.K_r:
                self.chess_model.game_state = GameState()
                self.chess_model.valid_moves = self.chess_model.game_state.get_valid_moves()
                self.chess_model.square_selected = ()
                self.chess_model.player_clicks = []
                self.chess_model.animate = False
                self.chess_model.move_made = False
                self.chess_model.game_over = False
                self.chess_model.game_state.check_mate = False
                self.chess_model.game_state.stale_mate = False
            if event.key == p.K_q:
                self.chess_model.running = False
                self.chess_model.game_over = True
                sys.exit()

        # view part

        if self.chess_model.move_made:
            if self.chess_model.animate:
                self.chess_view.animate_move(self.chess_model.game_state.move_log[-1], self.chess_view.screen,
                                             self.chess_model.game_state.board, self.chess_view.clock)
            self.chess_model.valid_moves = self.chess_model.game_state.get_valid_moves()
            self.chess_model.move_made = False
            self.chess_model.animate = False
            self.end_game(screen)

    def handle_menu_input(self, event):
        """
        Handles user input in the chess game menu.

        Args:
            - event: The Pygame event to be handled.
        """

        # Quit the game
        if event.type == p.QUIT:
            self.chess_view.game_situation = "quit"
            sys.exit()
        if event.type == p.KEYDOWN and event.key == p.K_ESCAPE:
            self.chess_view.game_situation = "quit"

        for button in menu.BUTTONS:
            button.check_click(event)

    def game_initialization(self, white_player, black_player, game_situation, running):
        """
        Initializes the game parameters, sending the settings selected in the menu interface.

        Args:
            - white_player (bool): True if the white player is human, False if AI.
            -  black_player (bool): True if the black player is human, False if AI.
            - game_situation (str): The initial game situation.
            - running (bool): True if the game is running, False otherwise.
        """
        self.chess_model.white_player = white_player
        self.chess_model.black_player = black_player
        self.chess_model.game_situation = game_situation
        self.chess_model.running = running
        self.chess_view.game_initialization()

    def end_game(self, screen):
        """
        Displays the end game message based on the game state.

        Args:
            - screen: The Pygame screen surface.
        """
        if self.chess_model.game_state.check_mate:
            self.chess_model.game_over = True
            if self.chess_model.game_state.white_to_move:
                view.draw_end_game(screen, "Black wins by checkmate")
            else:
                view.draw_end_game(screen, "White wins by checkmate")
        elif self.chess_model.game_state.stale_mate:
            self.chess_model.game_over = True
            view.draw_end_game(screen, "Stalemate")
