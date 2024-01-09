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
    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}

    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    cols_to_files = {v: k for k, v in files_to_cols.items()}

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
