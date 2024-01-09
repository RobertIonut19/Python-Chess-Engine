from Chess_Project.Chess.view import chess_view as view
from Chess_Project.Chess.controller import chess_controller as controller
import pygame as p


def main():
    chess_view = view.ChessView()
    chess_controller = controller.ChessController()


    while chess_controller.chess_model.running:
        for event in p.event.get():
            chess_controller.handle_input(chess_view.screen, event)

        chess_view.draw_board(chess_controller.chess_model.game_state, chess_controller.chess_model.square_selected)

        if chess_controller.chess_model.game_over:
            chess_controller.end_game(chess_view.screen)

        p.display.flip()
        chess_view.clock.tick(view.MAX_FPS)


if __name__ == "__main__":
    main()
