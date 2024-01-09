import sys

import pygame as p
from Chess_Project.Chess.model import chess_model as model
from Chess_Project.Chess.view import chess_view as view
from Chess_Project.Chess.view.chess_view import ChessView
from Chess_Project.Chess.model.moves.move_class import Move
from Chess_Project.Chess.model.moves.pieces_moves import random_move
from Chess_Project.Chess.model.game_state_class import GameState
class ChessController():
    def __init__(self):
        self.chess_model = model.ChessModel()
        self.chess_model.valid_moves = self.chess_model.game_state.get_valid_moves()
        self.chess_view = view.ChessView()



    def handle_input(self, screen, event):

        # model part

        human_turn = (self.chess_model.game_state.white_to_move and self.chess_model.white_player) or (not self.chess_model.game_state.white_to_move and self.chess_model.black_player)

        # Quit the game
        if event.type == p.QUIT:
            self.chess_model.running = False
        if event.type == p.KEYDOWN and event.key == p.K_ESCAPE: #posibila greseala
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
                        move = Move(self.chess_model.player_clicks[0], self.chess_model.player_clicks[1], self.chess_model.game_state.board)
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
            # if not self.chess_model.game_over and not human_turn:
            #     move = random_move(self.chess_model.valid_moves)
            #     self.chess_model.game_state.make_move(move)
            #     self.chess_model.game_state.move_log.append(move)
            #     self.chess_model.animate = True
            #     self.chess_model.move_made = True

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
                self.chess_view.animate_move(self.chess_model.game_state.move_log[-1], self.chess_view.screen, self.chess_model.game_state.board, self.chess_view.clock)
            self.chess_model.valid_moves = self.chess_model.game_state.get_valid_moves()
            self.chess_model.move_made = False
            self.chess_model.animate = False
            self.end_game(screen)

    def end_game(self, screen):
        if self.chess_model.game_state.check_mate:
            self.chess_model.game_over = True
            if self.chess_model.game_state.white_to_move:
                view.draw_end_game(screen, "Black wins by checkmate")
            else:
                view.draw_end_game(screen, "White wins by checkmate")
        elif self.chess_model.game_state.stale_mate:
            self.chess_model.game_over = True
            view.draw_end_game(screen, "Stalemate")
