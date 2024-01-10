from .move_class import Move


class CastleRights:
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


def get_castle_moves(gs, r, c, moves):
    """
        Get castle moves for the king at the specified position (r, c).

        Args:
            gs (GameState): The current game state.
            r (int): Row of the king.
            c (int): Column of the king.
            moves (list): List to store the generated moves.

        This method generates castle moves for the king at the specified position on the chessboard.
        It considers both king-side and queen-side castling moves if they are valid.
    """
    if gs.square_under_attack(r, c):
        return
    if ((gs.white_to_move and gs.current_castling_rights.wks) or
            (not gs.white_to_move and gs.current_castling_rights.bks)):
        get_king_side_castle_moves(gs.board, r, c, moves)
    if ((gs.white_to_move and gs.current_castling_rights.wqs) or
            (not gs.white_to_move and gs.current_castling_rights.bqs)):
        get_queen_side_castle_moves(gs.board, r, c, moves)


def get_king_side_castle_moves(gs, r, c, moves):
    """
        Get king-side castle moves for the king at the specified position (r, c).

        Args:
            gs (GameState): The current game state.
            r (int): Row of the king.
            c (int): Column of the king.
            moves (list): List to store the generated moves.

        This method generates king-side castle moves for the king at the specified position on the chessboard.

    """
    if gs.board[r][c+1] == '--' and gs.board[r][c+2] == '--':
        if not gs.square_under_attack(r, c+1) and not gs.square_under_attack(r, c+2):
            moves.append(Move((r, c), (r, c+2), gs.board, is_castle_move=True))


def get_queen_side_castle_moves(gs, r, c, moves):
    """
        Get queen-side castle moves for the king at the specified position (r, c).

        Args:
            gs (GameState): The current game state.
            r (int): Row of the king.
            c (int): Column of the king.
            moves (list): List to store the generated moves.

        This method generates queen-side castle moves for the king at the specified position on the chessboard.

    """
    if gs.board[r][c-1] == '--' and gs.board[r][c-2] == '--' and gs.board[r][c-3] == '--':
        if not gs.square_under_attack(r, c-1) and not gs.square_under_attack(r, c-2):
            moves.append(Move((r, c), (r, c-2), gs.board, is_castle_move=True))
