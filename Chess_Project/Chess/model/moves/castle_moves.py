from Chess_Project.Chess.model.moves.move_class import Move

class Castle_rights():
    def __init__(self, wks, bks, wqs, bqs):
        """
            Initialize the castling rights.

            Args:
                wks (bool): White kingside castling rights.
                bks (bool): Black kingside castling rights.
                wqs (bool): White queenside castling rights.
                bqs (bool): Black queenside castling rights.

            This class holds the castling rights for both players.
        """
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs


def get_castle_moves(white_to_move, r, c, moves):
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
        get_king_side_castle_moves(self.board, r, c, moves)
    if (self.white_to_move and self.current_castling_rights.wqs) or (not self.white_to_move and self.current_castling_rights.bqs):
        get_queen_side_castle_moves(self.board, r, c, moves)

def get_king_side_castle_moves(game_state, r, c, moves):
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

def get_queen_side_castle_moves(game_state, r, c, moves):
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
