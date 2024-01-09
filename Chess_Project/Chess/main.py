from Chess_Project.Chess.view import chess_view as view
from Chess_Project.Chess.controller import chess_controller as controller
import pygame as p


def main():
    chess_view = view.ChessView()
    chess_controller = controller.ChessController()

    # menu loop
    while chess_controller.chess_view.game_situation == "menu":
        for event in p.event.get():
            chess_controller.handle_menu_input(event)

        chess_view.draw(chess_controller.chess_model.game_state, chess_controller.chess_model.square_selected, chess_controller.chess_model.game_situation)

        p.display.flip()
        chess_view.clock.tick(view.MAX_FPS)

    chess_controller.game_initialization(chess_controller.chess_view.white_player, chess_controller.chess_view.black_player, chess_controller.chess_view.game_situation, chess_controller.chess_view.running)
    # game loop
    while chess_controller.chess_model.running and chess_controller.chess_model.game_situation == "game":
        for event in p.event.get():
            chess_controller.handle_input(chess_view.screen, event, chess_controller.chess_model.game_situation)

        chess_view.draw(chess_controller.chess_model.game_state, chess_controller.chess_model.square_selected)

        if chess_controller.chess_model.game_over:
            chess_controller.end_game(chess_view.screen)

        p.display.flip()
        chess_view.clock.tick(view.MAX_FPS)


if __name__ == "__main__":
    main()
