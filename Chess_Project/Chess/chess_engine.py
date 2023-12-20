"""
The GameState() class is responsible for storing all the information about the current state of a chess game.
It is responsible for checking if a move made by the user is valid and updating the board accordingly.
It records all the moves made so far.



"""



import copy as c

class GameState():
    def __init__(self):
        #board is an 8x8 matrix, representing the chess game board
        #"--" represents an empty space with no piece
        #in the name of each piece, there are two characters
        #first one represents the color of the piece
        #second one represents the type of the piece
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
        self.en_passant_possible = () #coordinates for the square where en-passant capture is possible

        self.current_castling_rights = Castle_rights(True, True, True, True)
        self.castle_rights_log = [Castle_rights(self.current_castling_rights.wks, self.current_castling_rights.bks,
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
        self.move_log.append(move) #for undo / history of the game
        self.white_to_move = not self.white_to_move #swap players

        if move.piece_moved == 'wK':
            self.white_king_location = (move.end_row, move.end_col)
        elif move.piece_moved == 'bK':
            self.black_king_location = (move.end_row, move.end_col)

        if move.is_pawn_promotion:
            self.board[move.end_row][move.end_col] = move.piece_moved[0] + 'Q' #iau culoarea si pun o regina la moment

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
        self.castle_rights_log.append(Castle_rights(self.current_castling_rights.wks, self.current_castling_rights.bks,
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

            Args:
                None

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

        self.castle_rights_log.pop() #remove the last castle rights from the log
        new_rights = c.deepcopy(self.castle_rights_log[-1])
        self.current_castling_rights = new_rights

        if move.is_castle_move:
            if move.end_col - move.start_col == 2: #kingside
                self.board[move.end_row][move.end_col+1] = self.board[move.end_row][move.end_col-1]
                self.board[move.end_row][move.end_col-1] = "--"
            else: #queenside
                self.board[move.end_row][move.end_col-2] = self.board[move.end_row][move.end_col+1]
                self.board[move.end_row][move.end_col+1] = "--"

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

    def get_valid_moves(self):
        """
            Get all valid moves considering checks.

            Returns:
                list: List of valid ChessMove objects.

            This method retrieves all possible moves and filters out those that would leave
            the current player in check. It also checks for checkmate and stalemate conditions.
        """

        temp_en_passant_possible = self.en_passant_possible
        temp_castle_rights = Castle_rights(self.current_castling_rights.wks, self.current_castling_rights.bks,
                                            self.current_castling_rights.wqs, self.current_castling_rights.bqs)
        moves = self.get_all_possible_moves()
        if self.white_to_move:
            self.get_castle_moves(self.white_king_location[0], self.white_king_location[1], moves)
        else:
            self.get_castle_moves(self.black_king_location[0], self.black_king_location[1], moves)

        for i in range(len(moves)-1, -1, -1):
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
        self.current_castling_rights = temp_castle_rights
        return moves

    def in_check(self):
        """
            Check if the current player is in check.

            Returns:
                bool: True if the current player is in check, False otherwise.

            This method determines whether the current player (either white or black) is in a state of check.
            It checks if the square occupied by the player's king is under attack by any opponent piece.

            Note: This method does not consider checkmate or stalemate conditions.

            Args:
                None
        """
        if self.white_to_move:
            return self.square_under_attack(self.white_king_location[0], self.white_king_location[1])
        else:
            return self.square_under_attack(self.black_king_location[0], self.black_king_location[1])

    def square_under_attack(self, r, c):
        """
    Determine if the square at position (r, c) is under attack by the opponent.

    Args:
        r (int): The row index of the square.
        c (int): The column index of the square.

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
            if move.end_row == r and move.end_col == c:
                return True
        return False

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
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0] #get the color of the piece - w or b
                if (turn == 'w' and self.white_to_move ) or (turn == 'b' and not self.white_to_move): #verifica later on
                    piece = self.board[r][c][1]
                    self.move_functions[piece](r, c, moves) #call the appropriate move function based on piece type
        return moves

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
            if self.board[r-1][c] == "--": #one square pawn advance
                moves.append(Move((r, c), (r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == "--":
                    moves.append(Move((r, c), (r-2, c), self.board)) #two square pawn advance - first move
            if c-1 >= 0:
                if self.board[r-1][c-1][0] == 'b':
                    moves.append(Move((r, c), (r-1, c-1), self.board))
                elif (r-1, c-1) == self.en_passant_possible:
                    moves.append(Move((r,c), (r-1, c-1), self.board, enpassant_possible=True))

            if c+1 <= 7:
                if self.board[r-1][c+1][0] == 'b':
                    moves.append(Move((r, c), (r-1, c+1), self.board))
                elif (r-1, c+1) == self.en_passant_possible:
                    moves.append(Move((r,c), (r-1, c+1), self.board, enpassant_possible=True))
        else:
            if self.board[r+1][c] == "--": #one square pawn advance
                moves.append(Move((r, c), (r+1, c), self.board))
                if r == 1 and self.board[r+2][c] == "--":
                    moves.append(Move((r, c), (r+2, c), self.board))
            if c-1 >= 0:
                if self.board[r+1][c-1][0] == 'w':
                    moves.append(Move((r, c), (r+1, c-1), self.board))
                elif ((r+1, c-1) == self.en_passant_possible):
                    moves.append(Move((r,c), (r+1, c-1), self.board, enpassant_possible=True))
            if c+1 <= 7:
                if self.board[r+1][c+1][0] == 'w':
                    moves.append(Move((r, c), (r+1, c+1), self.board))
                elif (r+1, c+1) == self.en_passant_possible:
                    moves.append(Move((r,c), (r+1, c+1), self.board, enpassant_possible=True))

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
            for row in range(r-1, -1, -1):
                if self.board[row][c] == "--":
                    moves.append(Move((r, c), (row, c), self.board))
                elif self.board[row][c][0] == 'b':
                    moves.append(Move((r, c), (row, c), self.board))
                    break
                else:
                    break
            for row in range(r+1, 8):
                if self.board[row][c] == "--":
                    moves.append(Move((r, c), (row, c), self.board))
                elif self.board[row][c][0] == 'b':
                    moves.append(Move((r, c), (row, c), self.board))
                    break
                else:
                    break
            for col in range(c-1, -1, -1):
                if self.board[r][col] == "--":
                    moves.append(Move((r, c), (r, col), self.board))
                elif self.board[r][col][0] == 'b':
                    moves.append(Move((r, c), (r, col), self.board))
                    break
                else:
                    break
            for col in range(c+1, 8):
                if self.board[r][col] == "--":
                    moves.append(Move((r, c), (r, col), self.board))
                elif self.board[r][col][0] == 'b':
                    moves.append(Move((r, c), (r, col), self.board))
                    break
                else:
                    break
        else:
            for row in range(r-1, -1, -1):
                if self.board[row][c] == "--":
                    moves.append(Move((r, c), (row, c), self.board))
                elif self.board[row][c][0] == 'w':
                    moves.append(Move((r, c), (row, c), self.board))
                    break
                else:
                    break
            for row in range(r+1, 8):
                if self.board[row][c] == "--":
                    moves.append(Move((r, c), (row, c), self.board))
                elif self.board[row][c][0] == 'w':
                    moves.append(Move((r, c), (row, c), self.board))
                    break
                else:
                    break
            for col in range(c-1, -1, -1):
                if self.board[r][col] == "--":
                    moves.append(Move((r, c), (r, col), self.board))
                elif self.board[r][col][0] == 'w':
                    moves.append(Move((r, c), (r, col), self.board))
                    break
                else:
                    break
            for col in range(c+1, 8):
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
            if r-2 >= 0 and c-1 >= 0:
                if self.board[r-2][c-1] == "--":
                    moves.append(Move((r, c), (r-2, c-1), self.board))
                elif self.board[r-2][c-1][0] == 'b':
                    moves.append(Move((r, c), (r-2, c-1), self.board))
            if r-2 >= 0 and c+1 <= 7:
                if self.board[r-2][c+1] == "--":
                    moves.append(Move((r, c), (r-2, c+1), self.board))
                elif self.board[r-2][c+1][0] == 'b':
                    moves.append(Move((r, c), (r-2, c+1), self.board))
            if r-1 >= 0 and c-2 >= 0:
                if self.board[r-1][c-2] == "--":
                    moves.append(Move((r, c), (r-1, c-2), self.board))
                elif self.board[r-1][c-2][0] == 'b':
                    moves.append(Move((r, c), (r-1, c-2), self.board))
            if r-1 >= 0 and c+2 <= 7:
                if self.board[r-1][c+2] == "--":
                    moves.append(Move((r, c), (r-1, c+2), self.board))
                elif self.board[r-1][c+2][0] == 'b':
                    moves.append(Move((r, c), (r-1, c+2), self.board))
            if r+1 <= 7 and c-2 >= 0:
                if self.board[r+1][c-2] == "--":
                    moves.append(Move((r, c), (r+1, c-2), self.board))
                elif self.board[r+1][c-2][0] == 'b':
                    moves.append(Move((r, c), (r+1, c-2), self.board))
            if r+1 <= 7 and c+2 <= 7:
                if self.board[r+1][c+2] == "--":
                    moves.append(Move((r, c), (r+1, c+2), self.board))
                elif self.board[r+1][c+2][0] == 'b':
                    moves.append(Move((r, c), (r+1, c+2), self.board))
            if r+2 <= 7 and c-1 >= 0:
                if self.board[r+2][c-1] == "--":
                    moves.append(Move((r, c), (r+2, c-1), self.board))
                elif self.board[r+2][c-1][0] == 'b':
                    moves.append(Move((r, c), (r+2, c-1), self.board))
            if r+2 <= 7 and c+1 <= 7:
                if self.board[r+2][c+1] == "--":
                    moves.append(Move((r, c), (r+2, c+1), self.board))
                elif self.board[r+2][c+1][0] == 'b':
                    moves.append(Move((r, c), (r+2, c+1), self.board))
        else:
            if r-2 >= 0 and c-1 >= 0:
                if self.board[r-2][c-1] == "--":
                    moves.append(Move((r, c), (r-2, c-1), self.board))
                elif self.board[r-2][c-1][0] == 'w':
                    moves.append(Move((r, c), (r-2, c-1), self.board))
            if r-2 >= 0 and c+1 <= 7:
                if self.board[r-2][c+1] == "--":
                    moves.append(Move((r, c), (r-2, c+1), self.board))
                elif self.board[r-2][c+1][0] == 'w':
                    moves.append(Move((r, c), (r-2, c+1), self.board))
            if r-1 >= 0 and c-2 >= 0:
                if self.board[r-1][c-2] == "--":
                    moves.append(Move((r, c), (r-1, c-2), self.board))
                elif self.board[r-1][c-2][0] == 'w':
                    moves.append(Move((r, c), (r-1, c-2), self.board))
            if r-1 >= 0 and c+2 <= 7:
                if self.board[r-1][c+2] == "--":
                    moves.append(Move((r, c), (r-1, c+2), self.board))
                elif self.board[r-1][c+2][0] == 'w':
                    moves.append(Move((r, c), (r-1, c+2), self.board))
            if r+1 <= 7 and c-2 >= 0:
                if self.board[r+1][c-2] == "--":
                    moves.append(Move((r, c), (r+1, c-2), self.board))
                elif self.board[r+1][c-2][0] == 'w':
                    moves.append(Move((r, c), (r+1, c-2), self.board))
            if r+1 <= 7 and c+2 <= 7:
                if self.board[r+1][c+2] == "--":
                    moves.append(Move((r, c), (r+1, c+2), self.board))
                elif self.board[r+1][c+2][0] == 'w':
                    moves.append(Move((r, c), (r+1, c+2), self.board))
            if r+2 <= 7 and c-1 >= 0:
                if self.board[r+2][c-1] == "--":
                    moves.append(Move((r, c), (r+2, c-1), self.board))
                elif self.board[r+2][c-1][0] == 'w':
                    moves.append(Move((r, c), (r+2, c-1), self.board))
            if r+2 <= 7 and c+1 <= 7:
                if self.board[r+2][c+1] == "--":
                    moves.append(Move((r, c), (r+2, c+1), self.board))
                elif self.board[r+2][c+1][0] == 'w':
                    moves.append(Move((r, c), (r+2, c+1), self.board))

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
                if r-i >= 0 and c-i >= 0:
                    if self.board[r-i][c-i] == "--":
                        moves.append(Move((r, c), (r-i, c-i), self.board))
                    elif self.board[r-i][c-i][0] == 'b':
                        moves.append(Move((r, c), (r-i, c-i), self.board))
                        break
                    else:
                        break
            for i in range(1, 8):
                if r-i >= 0 and c+i <= 7:
                    if self.board[r-i][c+i] == "--":
                        moves.append(Move((r, c), (r-i, c+i), self.board))
                    elif self.board[r-i][c+i][0] == 'b':
                        moves.append(Move((r, c), (r-i, c+i), self.board))
                        break
                    else:
                        break
            for i in range(1, 8):
                if r+i <= 7 and c-i >= 0:
                    if self.board[r+i][c-i] == "--":
                        moves.append(Move((r, c), (r+i, c-i), self.board))
                    elif self.board[r+i][c-i][0] == 'b':
                        moves.append(Move((r, c), (r+i, c-i), self.board))
                        break
                    else:
                        break
            for i in range(1, 8):
                if r+i <= 7 and c+i <= 7:
                    if self.board[r+i][c+i] == "--":
                        moves.append(Move((r, c), (r+i, c+i), self.board))
                    elif self.board[r+i][c+i][0] == 'b':
                        moves.append(Move((r, c), (r+i, c+i), self.board))
                        break
                    else:
                        break
        else:
            for i in range(1, 8):
                if r-i >= 0 and c-i >= 0:
                    if self.board[r-i][c-i] == "--":
                        moves.append(Move((r, c), (r-i, c-i), self.board))
                    elif self.board[r-i][c-i][0] == 'w':
                        moves.append(Move((r, c), (r-i, c-i), self.board))
                        break
                    else:
                        break
            for i in range(1, 8):
                if r-i >= 0 and c+i <= 7:
                    if self.board[r-i][c+i] == "--":
                        moves.append(Move((r, c), (r-i, c+i), self.board))
                    elif self.board[r-i][c+i][0] == 'w':
                        moves.append(Move((r, c), (r-i, c+i), self.board))
                        break
                    else:
                        break
            for i in range(1, 8):
                if r+i <= 7 and c-i >= 0:
                    if self.board[r+i][c-i] == "--":
                        moves.append(Move((r, c), (r+i, c-i), self.board))
                    elif self.board[r+i][c-i][0] == 'w':
                        moves.append(Move((r, c), (r+i, c-i), self.board))
                        break
                    else:
                        break
            for i in range(1, 8):
                if r+i <= 7 and c+i <= 7:
                    if self.board[r+i][c+i] == "--":
                        moves.append(Move((r, c), (r+i, c+i), self.board))
                    elif self.board[r+i][c+i][0] == 'w':
                        moves.append(Move((r, c), (r+i, c+i), self.board))
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
            It considers the king's possible moves in all directions, checking for validity and capturing opponent pieces.

        """
        if self.white_to_move:
            if r-1 >= 0:
                if self.board[r-1][c] == "--":
                    moves.append(Move((r, c), (r-1, c), self.board))
                elif self.board[r-1][c][0] == 'b':
                    moves.append(Move((r, c), (r-1, c), self.board))
            if r-1 >= 0 and c-1 >= 0:
                if self.board[r-1][c-1] == "--":
                    moves.append(Move((r, c), (r-1, c-1), self.board))
                elif self.board[r-1][c-1][0] == 'b':
                    moves.append(Move((r, c), (r-1, c-1), self.board))
            if r-1 >= 0 and c+1 <= 7:
                if self.board[r-1][c+1] == "--":
                    moves.append(Move((r, c), (r-1, c+1), self.board))
                elif self.board[r-1][c+1][0] == 'b':
                    moves.append(Move((r, c), (r-1, c+1), self.board))
            if c-1 >= 0:
                if self.board[r][c-1] == "--":
                    moves.append(Move((r, c), (r, c-1), self.board))
                elif self.board[r][c-1][0] == 'b':
                    moves.append(Move((r, c), (r, c-1), self.board))
            if c+1 <= 7:
                if self.board[r][c+1] == "--":
                    moves.append(Move((r, c), (r, c+1), self.board))
                elif self.board[r][c+1][0] == 'b':
                    moves.append(Move((r, c), (r, c+1), self.board))
            if r+1 <= 7:
                if self.board[r+1][c] == "--":
                    moves.append(Move((r, c), (r+1, c), self.board))
                elif self.board[r+1][c][0] == 'b':
                    moves.append(Move((r, c), (r+1, c), self.board))
            if r+1 <= 7 and c-1 >= 0:
                if self.board[r+1][c-1] == "--":
                    moves.append(Move((r, c), (r+1, c-1), self.board))
                elif self.board[r+1][c-1][0] == 'b':
                    moves.append(Move((r, c), (r+1, c-1), self.board))
            if r+1 <= 7 and c+1 <= 7:
                if self.board[r+1][c+1] == "--":
                    moves.append(Move((r, c), (r+1, c+1), self.board))
                elif self.board[r+1][c+1][0] == 'b':
                    moves.append(Move((r, c), (r+1, c+1), self.board))
        else:
            if r-1 >= 0:
                if self.board[r-1][c] == "--":
                    moves.append(Move((r, c), (r-1, c), self.board))
                elif self.board[r-1][c][0] == 'w':
                    moves.append(Move((r, c), (r-1, c), self.board))
            if r-1 >= 0 and c-1 >= 0:
                if self.board[r-1][c-1] == "--":
                    moves.append(Move((r, c), (r-1, c-1), self.board))
                elif self.board[r-1][c-1][0] == 'w':
                    moves.append(Move((r, c), (r-1, c-1), self.board))
            if r-1 >= 0 and c+1 <= 7:
                if self.board[r-1][c+1] == "--":
                    moves.append(Move((r, c), (r-1, c+1), self.board))
                elif self.board[r-1][c+1][0] == 'w':
                    moves.append(Move((r, c), (r-1, c+1), self.board))
            if c-1 >= 0:
                if self.board[r][c-1] == "--":
                    moves.append(Move((r, c), (r, c-1), self.board))
                elif self.board[r][c-1][0] == 'w':
                    moves.append(Move((r, c), (r, c-1), self.board))
            if c+1 <= 7:
                if self.board[r][c+1] == "--":
                    moves.append(Move((r, c), (r, c+1), self.board))
                elif self.board[r][c+1][0] == 'w':
                    moves.append(Move((r, c), (r, c+1), self.board))
            if r+1 <= 7:
                if self.board[r+1][c] == "--":
                    moves.append(Move((r, c), (r+1, c), self.board))
                elif self.board[r+1][c][0] == 'w':
                    moves.append(Move((r, c), (r+1, c), self.board))
            if r+1 <= 7 and c-1 >= 0:
                if self.board[r+1][c-1] == "--":
                    moves.append(Move((r, c), (r+1, c-1), self.board))
                elif self.board[r+1][c-1][0] == 'w':
                    moves.append(Move((r, c), (r+1, c-1), self.board))
            if r+1 <= 7 and c+1 <= 7:
                if self.board[r+1][c+1] == "--":
                    moves.append(Move((r, c), (r+1, c+1), self.board))
                elif self.board[r+1][c+1][0] == 'w':
                    moves.append(Move((r, c), (r+1, c+1), self.board))

    def get_castle_moves(self, r, c, moves):
        """
            Get castle moves for the king at the specified position (r, c).

            Args:
                r (int): Row of the king.
                c (int): Column of the king.
                moves (list): List to store the generated moves.

            This method generates castle moves for the king at the specified position on the chessboard.
            It considers both king-side and queen-side castling moves if they are valid.

        """
        if self.square_under_attack(r, c):
            return
        if (self.white_to_move and self.current_castling_rights.wks) or (not self.white_to_move and self.current_castling_rights.bks):
            self.get_king_side_castle_moves(r, c, moves)
        if (self.white_to_move and self.current_castling_rights.wqs) or (not self.white_to_move and self.current_castling_rights.bqs):
            self.get_queen_side_castle_moves(r, c, moves)

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


class Castle_rights():
    def __init__(self, wks, bks, wqs, bqs):
        """
                Initialize the castling rights.

                Args:
                    wks (bool): White kingside castling rights.
                    bks (bool): Black kingside castling rights.
                    wqs (bool): White queenside castling rights.
                    bqs (bool): Black queenside castling rights.

                This class represents the castling rights for both players.
        """
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs

class Move:
    """
    Represents a chess move.

    Attributes:
        start_row (int): Starting row of the move.
        start_col (int): Starting column of the move.
        end_row (int): Ending row of the move.
        end_col (int): Ending column of the move.
        piece_moved (str): Piece being moved (e.g., 'wp' for white pawn).
        piece_captured (str): Piece captured during the move.
        move_id (int): Unique identifier for the move.
        is_pawn_promotion (bool): Indicates if the move is a pawn promotion.
        is_en_passant_move (bool): Indicates if the move is an en passant capture.
        is_castle_move (bool): Indicates if the move is a castling move.

    Methods:
        __eq__(self, other): Overrides the equals method for Move objects.
        get_chess_notation(self): Returns the move in chess notation.
        get_rank_file(self, row, col): Converts row and column to chess rank and file notation.

    """
    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4,
                     "5": 3, "6": 2, "7": 1, "8": 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}  # reverse the dictionary

    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3,
                     "e": 4, "f": 5, "g": 6, "h": 7}
    cols_to_files = {v: k for k, v in files_to_cols.items()}  # reverse the dictionary

    def __init__(self, start_square, end_square, board, enpassant_possible=False, is_castle_move=False):
        """
        Initializes a Move object.

        Args:
            start_square (tuple): Starting square of the move (row, column).
            end_square (tuple): Ending square of the move (row, column).
            board (list): The current chess board.
            enpassant_possible (bool): Indicates if en passant capture is possible.
            is_castle_move (bool): Indicates if the move is a castling move.

        """
        self.start_row, self.start_col = start_square
        self.end_row, self.end_col = end_square

        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]

        self.move_id = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col

        self.is_pawn_promotion = False
        if (self.piece_moved == 'wp' and self.end_row == 0) or (self.piece_moved == 'bp' and self.end_row == 7):
            self.is_pawn_promotion = True

        self.is_en_passant_move = enpassant_possible
        if self.is_en_passant_move:
            self.piece_captured = 'wp' if self.piece_moved == 'bp' else 'bp'

        self.is_castle_move = is_castle_move

    def __eq__(self, other):
        """
        Overrides the equals method for Move objects.

        Args:
            other (Move): Another Move object to compare.

        Returns:
            bool: True if the moves are equal, False otherwise.

        """
        if isinstance(other, Move):
            return self.move_id == other.move_id
        return False

    def get_chess_notation(self):
        """
        Returns the move in chess notation.

        Returns:
            str: Chess notation for the move.

        """
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)

    def get_rank_file(self, row, col):
        """
        Converts row and column to chess rank and file notation.

        Args:
            row (int): Row index.
            col (int): Column index.

        Returns:
            str: Chess rank and file notation.

        """
        return self.cols_to_files[col] + self.rows_to_ranks[row]
