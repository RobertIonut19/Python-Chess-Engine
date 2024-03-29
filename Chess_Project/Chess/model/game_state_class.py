from .moves.castle_moves import CastleRights
from .moves.move_class import Move
import copy as c
import random


class GameState:
    """
    Represents the state of a chess game, including the current board configuration, player turns,
    and game-specific attributes such as castling rights, en passant possibilities, and check/mate conditions.

    Attributes:
        - board (list): A 2D list representing the current chessboard configuration.
        - move_functions (dict): A dictionary mapping piece types to their respective move generation functions.
        - white_to_move (bool): True if it's currently white's turn, False if black's turn.
        - move_log (list): A list to store the history of moves made during the game.
        - white_king_location (tuple): The current location of the white king on the board.
        - black_king_location (tuple): The current location of the black king on the board.
        - check_mate (bool): True if the current player is in checkmate, False otherwise.
        - stale_mate (bool): True if the game is in a stalemate position, False otherwise.
        - en_passant_possible (tuple): Coordinates for the square where en passant capture is possible.
        - current_castling_rights (CastleRights): An instance of the CastleRights class representing current castling rights.
        - CastleRights_log (list): A list to store the history of castling rights during the game.

    Methods:
        - make_move(move): Executes the given chess move on the board, updating the game state.
        - undo_move(): Undoes the last move made in the chess game, reverting the board to its previous state.
        - get_all_possible_moves(): Generates all possible moves for the current player without considering checks.
        - get_valid_moves(): Generates all valid moves considering checks, checkmate, and stalemate conditions.
        - in_check(): Checks if the current player is in check.
        - square_under_attack(r, col): Determines if the square at position (r, col) is under attack by the opponent.
        - update_castle_rights(move): Updates castle rights based on the given move.
        - get_castle_moves(r, col, moves): Generates castle moves for the king at the specified position (r, col).
        - get_king_side_castle_moves(r, c, moves): Generates king-side castle moves for the king at the specified position.
        - get_queen_side_castle_moves(r, c, moves): Generates queen-side castle moves for the king at the specified position.
        - get_pawn_moves(r, c, moves): Generates all possible moves for a pawn at the given position (r, c).
        - get_rook_moves(r, c, moves): Generates all possible moves for a rook at the given position (r, c).
        - get_knight_moves(r, c, moves): Generates all possible moves for a knight at the given position (r, c).
        - get_bishop_moves(r, c, moves): Generates all possible moves for a bishop at the given position (r, c).
        - get_queen_moves(r, c, moves): Generates all possible moves for a queen at the given position (r, c).
        - get_king_moves(r, c, moves): Generates all possible moves for a king at the given position (r, c).
        - random_move(valid_moves): Generates a random move from the list of valid moves.

    """
    def __init__(self):
        """
            Initialize the game state.
        """
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]

        self.move_functions = {'p': self.get_pawn_moves, 'R': self.get_rook_moves, 'N': self.get_knight_moves,
                               'B': self.get_bishop_moves, 'Q': self.get_queen_moves, 'K': self.get_king_moves}
        self.white_to_move = True
        self.move_log = []
        self.white_king_location = (7, 4)
        self.black_king_location = (0, 4)
        self.check_mate = False
        self.stale_mate = False
        self.en_passant_possible = ()  # coordinates for the square where en-passant capture is possible

        self.current_castling_rights = CastleRights(True, True, True, True)
        self.CastleRights_log = [CastleRights(self.current_castling_rights.wks, self.current_castling_rights.bks,
                                              self.current_castling_rights.wqs, self.current_castling_rights.bqs)]

    def make_move(self, move):
        """
        Executes the given chess move on the board.

        Parameters:
            move (ChessMove): The move to be executed.

        Returns:
            None

        Raises:
            None

        This method updates the game state by modifying the chess board, updating the move log,
        and adjusting various game attributes. It handles regular moves, captures, castling, pawn promotion,
        and en-passant moves.

        Args:
            move (ChessMove): The move object containing information about the move.

        - Regular Moves:
            - Moves the piece from the starting position to the ending position on the chess board.
            - Updates the move log.

        - Pawn Promotion:
            - If the move involves pawn promotion, replaces the pawn with a queen.

        - En-passant:
            - If the move is an en-passant capture, removes the captured pawn.

        - Castling:
            - If the move involves castling, adjusts the rook position accordingly.

        - Update King Positions:
            - Updates the current positions of kings if they are moved.

        - Update En-passant Possibility:
            - Sets or clears the possibility of en-passant capture.

        - Update Castle Rights:
            - Updates the castle rights after each move.

        - Update Turn:
            - Changes the player turn to the next player.
        """
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)  # for undo / history of the game
        self.white_to_move = not self.white_to_move  # swap players

        if move.piece_moved == 'wK':
            self.white_king_location = (move.end_row, move.end_col)
        elif move.piece_moved == 'bK':
            self.black_king_location = (move.end_row, move.end_col)

        if move.is_pawn_promotion:
            self.board[move.end_row][move.end_col] = move.piece_moved[0] + 'Q'  # iau culoarea si pun o regina la moment

        if move.is_en_passant_move:
            self.board[move.start_row][move.end_col] = "--"

        if move.piece_moved[1] == 'p' and abs(move.start_row - move.end_row) == 2:
            self.en_passant_possible = ((move.start_row + move.end_row)//2, move.start_col)
        else:
            self.en_passant_possible = ()

        if move.is_castle_move:
            if move.end_col - move.start_col == 2:
                self.board[move.end_row][move.end_col-1] = self.board[move.end_row][move.end_col+1]
                self.board[move.end_row][move.end_col+1] = "--"
            else:
                self.board[move.end_row][move.end_col+1] = self.board[move.end_row][move.end_col-2]
                self.board[move.end_row][move.end_col-2] = "--"

        self.update_castle_rights(move)
        self.CastleRights_log.append(CastleRights(self.current_castling_rights.wks, self.current_castling_rights.bks,
                                                  self.current_castling_rights.wqs, self.current_castling_rights.bqs))

    def undo_move(self):
        """
            Undo the last move made in the chess game.

            Returns:
                None

            Raises:
                IndexError: If there are no moves to undo.

            This method reverses the effects of the last move by restoring the board to its previous state.
            It updates piece positions, player turns, en-passant possibilities, and castle rights.

            - Restore Board:
                - Restores the board to its previous state by reversing the effects of the last move.
        """
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.white_to_move = not self.white_to_move
            if move.piece_moved == 'wK':
                self.white_king_location = (move.start_row, move.start_col)
            elif move.piece_moved == 'bK':
                self.black_king_location = (move.start_row, move.start_col)

            if move.is_en_passant_move:
                self.board[move.end_row][move.end_col] = "--"
                self.board[move.start_row][move.end_col] = move.piece_captured
                self.en_passant_possible = (move.end_row, move.end_col)

            if move.piece_moved[1] == 'p' and abs(move.start_row - move.end_row) == 2:
                self.en_passant_possible = ()

            self.CastleRights_log.pop()  # remove the last castle rights from the log
            new_rights = c.deepcopy(self.CastleRights_log[-1])
            self.current_castling_rights = new_rights

            if move.is_castle_move:
                if move.end_col - move.start_col == 2:  # kingside
                    self.board[move.end_row][move.end_col + 1] = self.board[move.end_row][move.end_col - 1]
                    self.board[move.end_row][move.end_col - 1] = "--"
                else:  # queenside
                    self.board[move.end_row][move.end_col - 2] = self.board[move.end_row][move.end_col + 1]
                    self.board[move.end_row][move.end_col + 1] = "--"

    def get_all_possible_moves(self):
        """
            Get all possible moves for the current player without considering checks.

            Returns:
                list: A list of all possible moves.

            This method generates all possible moves for the current player on the chessboard without considering
            whether the moves result in a check. It iterates through all squares on the board, identifies the color
            and type of the piece on each square, and calls the corresponding move function.
        """
        moves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                turn = self.board[row][col][0]  # get the color of the piece - w or b
                if (turn == 'w' and self.white_to_move) or (
                        turn == 'b' and not self.white_to_move):
                    piece = self.board[row][col][1]
                    self.move_functions[piece](row, col, moves)  # call the right move function based on piece type
        return moves

    def get_valid_moves(self):
        """
            Get all valid moves considering checks.

            Returns:
                list: List of valid ChessMove objects.

            This method retrieves all possible moves and filters out those that would leave
            the current player in check. It also checks for checkmate and stalemate conditions.
        """

        temp_en_passant_possible = self.en_passant_possible
        temp_CastleRights = CastleRights(self.current_castling_rights.wks, self.current_castling_rights.bks,
                                         self.current_castling_rights.wqs, self.current_castling_rights.bqs)
        moves = self.get_all_possible_moves()
        if self.white_to_move:
            self.get_castle_moves(self.white_king_location[0], self.white_king_location[1], moves)
        else:
            self.get_castle_moves(self.black_king_location[0], self.black_king_location[1], moves)

        for i in range(len(moves) - 1, -1, -1):
            self.make_move(moves[i])
            self.white_to_move = not self.white_to_move
            if self.in_check():
                moves.remove(moves[i])
            self.white_to_move = not self.white_to_move
            self.undo_move()
        if len(moves) == 0:
            if self.in_check():
                self.check_mate = True
            else:
                self.stale_mate = True
        else:
            self.check_mate = False
            self.stale_mate = False

        self.en_passant_possible = temp_en_passant_possible
        self.current_castling_rights = temp_CastleRights
        return moves

    def in_check(self):
        """
            Check if the current player is in check.

            Returns:
                bool: True if the current player is in check, False otherwise.

            This method determines whether the current player (either white or black) is in a state of check.
            It checks if the square occupied by the player's king is under attack by any opponent piece.

            Note: This method does not consider checkmate or stalemate conditions.

        """
        if self.white_to_move:
            return self.square_under_attack(self.white_king_location[0], self.white_king_location[1])
        else:
            return self.square_under_attack(self.black_king_location[0], self.black_king_location[1])

    def square_under_attack(self, r, col):
        """
        Determine if the square at position (r, c) is under attack by the opponent.

        Args:
            r (int): The row index of the square.
            col (int): The column index of the square.

        Returns:
            bool: True if the square is under attack, False otherwise.

        This method calculates whether the square at position (r, c) on the chessboard is under attack
        by any piece of the opponent. It does so by temporarily switching the turn to the opponent's side,
        obtaining all possible moves for the opponent, and checking if any of those moves target the specified square.
        """
        self.white_to_move = not self.white_to_move
        oppMoves = self.get_all_possible_moves()
        self.white_to_move = not self.white_to_move
        for move in oppMoves:
            if move.end_row == r and move.end_col == col:
                return True
        return False

    def update_castle_rights(self, move):
        """
            Update castle rights based on the given move.

            Args:
                move (ChessMove): The move for which castle rights need to be updated.

            Returns:
                None

            This method adjusts the castle rights after a move is made. It considers the movement
            of kings and rooks to determine whether castling is still possible for each side.

            Args:
                move (ChessMove): The move for which castle rights need to be updated.

            - Update White King Side Castle Rights:
                - If the white king moves, white loses the right to castle kingside.
                - If the white kingside rook moves, white loses the right to castle kingside.

            - Update White Queen Side Castle Rights:
                - If the white king moves, white loses the right to castle queenside.
                - If the white queenside rook moves, white loses the right to castle queenside.

            - Update Black King Side Castle Rights:
                - If the black king moves, black loses the right to castle kingside.
                - If the black kingside rook moves, black loses the right to castle kingside.

            - Update Black Queen Side Castle Rights:
                - If the black king moves, black loses the right to castle queenside.
                - If the black queenside rook moves, black loses the right to castle queenside.
            """
        if move.piece_moved == 'wK':
            self.current_castling_rights.wks = False
            self.current_castling_rights.wqs = False
        elif move.piece_moved == 'bK':
            self.current_castling_rights.bks = False
            self.current_castling_rights.bqs = False
        elif move.piece_moved == 'wR':
            if move.start_row == 7:
                if move.start_col == 0:
                    self.current_castling_rights.wqs = False
                elif move.start_col == 7:
                    self.current_castling_rights.wks = False
        elif move.piece_moved == 'bR':
            if move.start_row == 0:
                if move.start_col == 0:
                    self.current_castling_rights.bqs = False
                elif move.start_col == 7:
                    self.current_castling_rights.bks = False

        # if a rook is captured
        if move.piece_captured == 'wR':
            if move.end_row == 7:
                if move.end_col == 0:
                    self.current_castling_rights.wqs = False
                elif move.end_col == 7:
                    self.current_castling_rights.wks = False
        elif move.piece_captured == 'bR':
            if move.end_row == 0:
                if move.end_col == 0:
                    self.current_castling_rights.bqs = False
                elif move.end_col == 7:
                    self.current_castling_rights.bks = False

    def get_castle_moves(self, r, col, moves):
        """
            Get castle moves for the king at the specified position (r, c).

            Args:
                r (int): Row of the king.
                col (int): Column of the king.
                moves (list): List to store the generated moves.

            This method generates castle moves for the king at the specified position on the chessboard.
            It considers both king-side and queen-side castling moves if they are valid.

        """
        if self.square_under_attack(r, col):
            return
        if ((self.white_to_move and self.current_castling_rights.wks) or
                (not self.white_to_move and self.current_castling_rights.bks)):
            self.get_king_side_castle_moves(r, col, moves)
        if ((self.white_to_move and self.current_castling_rights.wqs) or
                (not self.white_to_move and self.current_castling_rights.bqs)):
            self.get_queen_side_castle_moves(r, col, moves)

    def get_king_side_castle_moves(self, r, c, moves):
        """
            Get king-side castle moves for the king at the specified position (r, c).

            Args:
                r (int): Row of the king.
                c (int): Column of the king.
                moves (list): List to store the generated moves.

            This method generates king-side castle moves for the king at the specified position on the chessboard.

        """
        if self.board[r][c+1] == '--' and self.board[r][c+2] == '--':
            if not self.square_under_attack(r, c+1) and not self.square_under_attack(r, c+2):
                moves.append(Move((r, c), (r, c+2), self.board, is_castle_move=True))

    def get_queen_side_castle_moves(self, r, c, moves):
        """
            Get queen-side castle moves for the king at the specified position (r, c).

            Args:
                r (int): Row of the king.
                c (int): Column of the king.
                moves (list): List to store the generated moves.

            This method generates queen-side castle moves for the king at the specified position on the chessboard.

        """
        if self.board[r][c-1] == '--' and self.board[r][c-2] == '--' and self.board[r][c-3] == '--':
            if not self.square_under_attack(r, c-1) and not self.square_under_attack(r, c-2):
                moves.append(Move((r, c), (r, c-2), self.board, is_castle_move=True))

    def get_pawn_moves(self, r, c, moves):
        """
           Get all possible moves for a pawn at the given position (r, c).

            Args:
                r (int): Row of the pawn.
                c (int): Column of the pawn.
                moves (list): List to store the generated moves.

            This method generates all possible moves for a pawn at the specified position on the chessboard.
            It considers one and two square advances, captures diagonally, and en passant captures.

        """
        if self.white_to_move:
            if self.board[r - 1][c] == "--":  # one square pawn advance
                moves.append(Move((r, c), (r - 1, c), self.board))
                if r == 6 and self.board[r - 2][c] == "--":
                    moves.append(Move((r, c), (r - 2, c), self.board))  # two square pawn advance - first move
            if c - 1 >= 0:
                if self.board[r - 1][c - 1][0] == 'b':
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
                elif (r - 1, c - 1) == self.en_passant_possible:
                    moves.append(Move((r, c), (r - 1, c - 1), self.board, enpassant_possible=True))

            if c + 1 <= 7:
                if self.board[r - 1][c + 1][0] == 'b':
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))
                elif (r - 1, c + 1) == self.en_passant_possible:
                    moves.append(Move((r, c), (r - 1, c + 1), self.board, enpassant_possible=True))
        else:
            if self.board[r + 1][c] == "--":  # one square pawn advance
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r + 2][c] == "--":
                    moves.append(Move((r, c), (r + 2, c), self.board))
            if c - 1 >= 0:
                if self.board[r + 1][c - 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
                elif (r + 1, c - 1) == self.en_passant_possible:
                    moves.append(Move((r, c), (r + 1, c - 1), self.board, enpassant_possible=True))
            if c + 1 <= 7:
                if self.board[r + 1][c + 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))
                elif (r + 1, c + 1) == self.en_passant_possible:
                    moves.append(Move((r, c), (r + 1, c + 1), self.board, enpassant_possible=True))

    def get_rook_moves(self, r, c, moves):
        """
            Get all possible moves for a rook at the given position (r, c).

            Args:
                r (int): Row of the rook.
                c (int): Column of the rook.
                moves (list): List to store the generated moves.

            This method generates all possible moves for a rook at the specified position on the chessboard.
            It considers moves along the rows and columns until it encounters a piece or the edge of the board.
        """
        if self.white_to_move:
            for row in range(r - 1, -1, -1):
                if self.board[row][c] == "--":
                    moves.append(Move((r, c), (row, c), self.board))
                elif self.board[row][c][0] == 'b':
                    moves.append(Move((r, c), (row, c), self.board))
                    break
                else:
                    break
            for row in range(r + 1, 8):
                if self.board[row][c] == "--":
                    moves.append(Move((r, c), (row, c), self.board))
                elif self.board[row][c][0] == 'b':
                    moves.append(Move((r, c), (row, c), self.board))
                    break
                else:
                    break
            for col in range(c - 1, -1, -1):
                if self.board[r][col] == "--":
                    moves.append(Move((r, c), (r, col), self.board))
                elif self.board[r][col][0] == 'b':
                    moves.append(Move((r, c), (r, col), self.board))
                    break
                else:
                    break
            for col in range(c + 1, 8):
                if self.board[r][col] == "--":
                    moves.append(Move((r, c), (r, col), self.board))
                elif self.board[r][col][0] == 'b':
                    moves.append(Move((r, c), (r, col), self.board))
                    break
                else:
                    break
        else:
            for row in range(r - 1, -1, -1):
                if self.board[row][c] == "--":
                    moves.append(Move((r, c), (row, c), self.board))
                elif self.board[row][c][0] == 'w':
                    moves.append(Move((r, c), (row, c), self.board))
                    break
                else:
                    break
            for row in range(r + 1, 8):
                if self.board[row][c] == "--":
                    moves.append(Move((r, c), (row, c), self.board))
                elif self.board[row][c][0] == 'w':
                    moves.append(Move((r, c), (row, c), self.board))
                    break
                else:
                    break
            for col in range(c - 1, -1, -1):
                if self.board[r][col] == "--":
                    moves.append(Move((r, c), (r, col), self.board))
                elif self.board[r][col][0] == 'w':
                    moves.append(Move((r, c), (r, col), self.board))
                    break
                else:
                    break
            for col in range(c + 1, 8):
                if self.board[r][col] == "--":
                    moves.append(Move((r, c), (r, col), self.board))
                elif self.board[r][col][0] == 'w':
                    moves.append(Move((r, c), (r, col), self.board))
                    break
                else:
                    break

    def get_knight_moves(self, r, c, moves):
        """
            Get all possible moves for a knight at the given position (r, c).

            Args:
                r (int): Row of the knight.
                c (int): Column of the knight.
                moves (list): List to store the generated moves.

            This method generates all possible moves for a knight at the specified position on the chessboard.
            It considers all eight possible knight moves, checking for validity and capturing opponent pieces.

            """
        if self.white_to_move:
            if r - 2 >= 0 and c - 1 >= 0:
                if self.board[r - 2][c - 1] == "--":
                    moves.append(Move((r, c), (r - 2, c - 1), self.board))
                elif self.board[r - 2][c - 1][0] == 'b':
                    moves.append(Move((r, c), (r - 2, c - 1), self.board))
            if r - 2 >= 0 and c + 1 <= 7:
                if self.board[r - 2][c + 1] == "--":
                    moves.append(Move((r, c), (r - 2, c + 1), self.board))
                elif self.board[r - 2][c + 1][0] == 'b':
                    moves.append(Move((r, c), (r - 2, c + 1), self.board))
            if r - 1 >= 0 and c - 2 >= 0:
                if self.board[r - 1][c - 2] == "--":
                    moves.append(Move((r, c), (r - 1, c - 2), self.board))
                elif self.board[r - 1][c - 2][0] == 'b':
                    moves.append(Move((r, c), (r - 1, c - 2), self.board))
            if r - 1 >= 0 and c + 2 <= 7:
                if self.board[r - 1][c + 2] == "--":
                    moves.append(Move((r, c), (r - 1, c + 2), self.board))
                elif self.board[r - 1][c + 2][0] == 'b':
                    moves.append(Move((r, c), (r - 1, c + 2), self.board))
            if r + 1 <= 7 and c - 2 >= 0:
                if self.board[r + 1][c - 2] == "--":
                    moves.append(Move((r, c), (r + 1, c - 2), self.board))
                elif self.board[r + 1][c - 2][0] == 'b':
                    moves.append(Move((r, c), (r + 1, c - 2), self.board))
            if r + 1 <= 7 and c + 2 <= 7:
                if self.board[r + 1][c + 2] == "--":
                    moves.append(Move((r, c), (r + 1, c + 2), self.board))
                elif self.board[r + 1][c + 2][0] == 'b':
                    moves.append(Move((r, c), (r + 1, c + 2), self.board))
            if r + 2 <= 7 and c - 1 >= 0:
                if self.board[r + 2][c - 1] == "--":
                    moves.append(Move((r, c), (r + 2, c - 1), self.board))
                elif self.board[r + 2][c - 1][0] == 'b':
                    moves.append(Move((r, c), (r + 2, c - 1), self.board))
            if r + 2 <= 7 and c + 1 <= 7:
                if self.board[r + 2][c + 1] == "--":
                    moves.append(Move((r, c), (r + 2, c + 1), self.board))
                elif self.board[r + 2][c + 1][0] == 'b':
                    moves.append(Move((r, c), (r + 2, c + 1), self.board))
        else:
            if r - 2 >= 0 and c - 1 >= 0:
                if self.board[r - 2][c - 1] == "--":
                    moves.append(Move((r, c), (r - 2, c - 1), self.board))
                elif self.board[r - 2][c - 1][0] == 'w':
                    moves.append(Move((r, c), (r - 2, c - 1), self.board))
            if r - 2 >= 0 and c + 1 <= 7:
                if self.board[r - 2][c + 1] == "--":
                    moves.append(Move((r, c), (r - 2, c + 1), self.board))
                elif self.board[r - 2][c + 1][0] == 'w':
                    moves.append(Move((r, c), (r - 2, c + 1), self.board))
            if r - 1 >= 0 and c - 2 >= 0:
                if self.board[r - 1][c - 2] == "--":
                    moves.append(Move((r, c), (r - 1, c - 2), self.board))
                elif self.board[r - 1][c - 2][0] == 'w':
                    moves.append(Move((r, c), (r - 1, c - 2), self.board))
            if r - 1 >= 0 and c + 2 <= 7:
                if self.board[r - 1][c + 2] == "--":
                    moves.append(Move((r, c), (r - 1, c + 2), self.board))
                elif self.board[r - 1][c + 2][0] == 'w':
                    moves.append(Move((r, c), (r - 1, c + 2), self.board))
            if r + 1 <= 7 and c - 2 >= 0:
                if self.board[r + 1][c - 2] == "--":
                    moves.append(Move((r, c), (r + 1, c - 2), self.board))
                elif self.board[r + 1][c - 2][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c - 2), self.board))
            if r + 1 <= 7 and c + 2 <= 7:
                if self.board[r + 1][c + 2] == "--":
                    moves.append(Move((r, c), (r + 1, c + 2), self.board))
                elif self.board[r + 1][c + 2][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c + 2), self.board))
            if r + 2 <= 7 and c - 1 >= 0:
                if self.board[r + 2][c - 1] == "--":
                    moves.append(Move((r, c), (r + 2, c - 1), self.board))
                elif self.board[r + 2][c - 1][0] == 'w':
                    moves.append(Move((r, c), (r + 2, c - 1), self.board))
            if r + 2 <= 7 and c + 1 <= 7:
                if self.board[r + 2][c + 1] == "--":
                    moves.append(Move((r, c), (r + 2, c + 1), self.board))
                elif self.board[r + 2][c + 1][0] == 'w':
                    moves.append(Move((r, c), (r + 2, c + 1), self.board))

    def get_bishop_moves(self, r, c, moves):
        """
            Get all possible moves for a bishop at the given position (r, c).

            Args:
                r (int): Row of the bishop.
                c (int): Column of the bishop.
                moves (list): List to store the generated moves.

                This method generates all possible moves for a bishop at the specified position on the chessboard.
                It considers all diagonal moves, checking for validity and capturing opponent pieces.

        """
        if self.white_to_move:
            for i in range(1, 8):
                if r - i >= 0 and c - i >= 0:
                    if self.board[r - i][c - i] == "--":
                        moves.append(Move((r, c), (r - i, c - i), self.board))
                    elif self.board[r - i][c - i][0] == 'b':
                        moves.append(Move((r, c), (r - i, c - i), self.board))
                        break
                    else:
                        break
            for i in range(1, 8):
                if r - i >= 0 and c + i <= 7:
                    if self.board[r - i][c + i] == "--":
                        moves.append(Move((r, c), (r - i, c + i), self.board))
                    elif self.board[r - i][c + i][0] == 'b':
                        moves.append(Move((r, c), (r - i, c + i), self.board))
                        break
                    else:
                        break
            for i in range(1, 8):
                if r + i <= 7 and c - i >= 0:
                    if self.board[r + i][c - i] == "--":
                        moves.append(Move((r, c), (r + i, c - i), self.board))
                    elif self.board[r + i][c - i][0] == 'b':
                        moves.append(Move((r, c), (r + i, c - i), self.board))
                        break
                    else:
                        break
            for i in range(1, 8):
                if r + i <= 7 and c + i <= 7:
                    if self.board[r + i][c + i] == "--":
                        moves.append(Move((r, c), (r + i, c + i), self.board))
                    elif self.board[r + i][c + i][0] == 'b':
                        moves.append(Move((r, c), (r + i, c + i), self.board))
                        break
                    else:
                        break
        else:
            for i in range(1, 8):
                if r - i >= 0 and c - i >= 0:
                    if self.board[r - i][c - i] == "--":
                        moves.append(Move((r, c), (r - i, c - i), self.board))
                    elif self.board[r - i][c - i][0] == 'w':
                        moves.append(Move((r, c), (r - i, c - i), self.board))
                        break
                    else:
                        break
            for i in range(1, 8):
                if r - i >= 0 and c + i <= 7:
                    if self.board[r - i][c + i] == "--":
                        moves.append(Move((r, c), (r - i, c + i), self.board))
                    elif self.board[r - i][c + i][0] == 'w':
                        moves.append(Move((r, c), (r - i, c + i), self.board))
                        break
                    else:
                        break
            for i in range(1, 8):
                if r + i <= 7 and c - i >= 0:
                    if self.board[r + i][c - i] == "--":
                        moves.append(Move((r, c), (r + i, c - i), self.board))
                    elif self.board[r + i][c - i][0] == 'w':
                        moves.append(Move((r, c), (r + i, c - i), self.board))
                        break
                    else:
                        break
            for i in range(1, 8):
                if r + i <= 7 and c + i <= 7:
                    if self.board[r + i][c + i] == "--":
                        moves.append(Move((r, c), (r + i, c + i), self.board))
                    elif self.board[r + i][c + i][0] == 'w':
                        moves.append(Move((r, c), (r + i, c + i), self.board))
                        break
                    else:
                        break

    def get_queen_moves(self, r, c, moves):
        """
        Get all possible moves for a queen at the given position (r, c).

        Args:
            r (int): Row of the queen.
            c (int): Column of the queen.
            moves (list): List to store the generated moves.

            This method generates all possible moves for a queen at the specified position on the chessboard.
            It combines the moves of a rook and a bishop, checking for validity and capturing opponent pieces.

        """
        self.get_rook_moves(r, c, moves)
        self.get_bishop_moves(r, c, moves)

    def get_king_moves(self, r, c, moves):
        """
            Get all possible moves for a king at the given position (r, c).

            Args:
                r (int): Row of the king.
                c (int): Column of the king.
                moves (list): List to store the generated moves.

            This method generates all possible moves for a king at the specified position on the chessboard.
            It considers the king possible moves in all directions, checking for validity and capturing opponent pieces

        """
        if self.white_to_move:
            if r - 1 >= 0:
                if self.board[r - 1][c] == "--":
                    moves.append(Move((r, c), (r - 1, c), self.board))
                elif self.board[r - 1][c][0] == 'b':
                    moves.append(Move((r, c), (r - 1, c), self.board))
            if r - 1 >= 0 and c - 1 >= 0:
                if self.board[r - 1][c - 1] == "--":
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
                elif self.board[r - 1][c - 1][0] == 'b':
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
            if r - 1 >= 0 and c + 1 <= 7:
                if self.board[r - 1][c + 1] == "--":
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))
                elif self.board[r - 1][c + 1][0] == 'b':
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))
            if c - 1 >= 0:
                if self.board[r][c - 1] == "--":
                    moves.append(Move((r, c), (r, c - 1), self.board))
                elif self.board[r][c - 1][0] == 'b':
                    moves.append(Move((r, c), (r, c - 1), self.board))
            if c + 1 <= 7:
                if self.board[r][c + 1] == "--":
                    moves.append(Move((r, c), (r, c + 1), self.board))
                elif self.board[r][c + 1][0] == 'b':
                    moves.append(Move((r, c), (r, c + 1), self.board))
            if r + 1 <= 7:
                if self.board[r + 1][c] == "--":
                    moves.append(Move((r, c), (r + 1, c), self.board))
                elif self.board[r + 1][c][0] == 'b':
                    moves.append(Move((r, c), (r + 1, c), self.board))
            if r + 1 <= 7 and c - 1 >= 0:
                if self.board[r + 1][c - 1] == "--":
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
                elif self.board[r + 1][c - 1][0] == 'b':
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
            if r + 1 <= 7 and c + 1 <= 7:
                if self.board[r + 1][c + 1] == "--":
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))
                elif self.board[r + 1][c + 1][0] == 'b':
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))
        else:
            if r - 1 >= 0:
                if self.board[r - 1][c] == "--":
                    moves.append(Move((r, c), (r - 1, c), self.board))
                elif self.board[r - 1][c][0] == 'w':
                    moves.append(Move((r, c), (r - 1, c), self.board))
            if r - 1 >= 0 and c - 1 >= 0:
                if self.board[r - 1][c - 1] == "--":
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
                elif self.board[r - 1][c - 1][0] == 'w':
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
            if r - 1 >= 0 and c + 1 <= 7:
                if self.board[r - 1][c + 1] == "--":
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))
                elif self.board[r - 1][c + 1][0] == 'w':
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))
            if c - 1 >= 0:
                if self.board[r][c - 1] == "--":
                    moves.append(Move((r, c), (r, c - 1), self.board))
                elif self.board[r][c - 1][0] == 'w':
                    moves.append(Move((r, c), (r, c - 1), self.board))
            if c + 1 <= 7:
                if self.board[r][c + 1] == "--":
                    moves.append(Move((r, c), (r, c + 1), self.board))
                elif self.board[r][c + 1][0] == 'w':
                    moves.append(Move((r, c), (r, c + 1), self.board))
            if r + 1 <= 7:
                if self.board[r + 1][c] == "--":
                    moves.append(Move((r, c), (r + 1, c), self.board))
                elif self.board[r + 1][c][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c), self.board))
            if r + 1 <= 7 and c - 1 >= 0:
                if self.board[r + 1][c - 1] == "--":
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
                elif self.board[r + 1][c - 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
            if r + 1 <= 7 and c + 1 <= 7:
                if self.board[r + 1][c + 1] == "--":
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))
                elif self.board[r + 1][c + 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))

    def random_move(self, valid_moves):
        """
        Generate a random move from the list of valid moves.

        Args:
            valid_moves (list): List of valid moves.

        Returns:
            ChessMove: A random move from the list of valid moves.
        """
        return valid_moves[random.randint(0, len(valid_moves) - 1)]
