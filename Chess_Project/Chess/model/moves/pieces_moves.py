from Chess_Project.Chess.model.moves.move_class import Move
from Chess_Project.Chess.model.game_state_class import GameState
import random

def get_pawn_moves(game_state : GameState, r, c, moves):
    """
       Get all possible moves for a pawn at the given position (r, c).

        Args:
            r (int): Row of the pawn.
            c (int): Column of the pawn.
            moves (list): List to store the generated moves.

        This method generates all possible moves for a pawn at the specified position on the chessboard.
        It considers one and two square advances, captures diagonally, and en passant captures.

    """
    if game_state.white_to_move:
        if game_state.board[r - 1][c] == "--":  # one square pawn advance
            moves.append(Move((r, c), (r - 1, c), game_state.board))
            if r == 6 and game_state.board[r - 2][c] == "--":
                moves.append(Move((r, c), (r - 2, c), game_state.board))  # two square pawn advance - first move
        if c - 1 >= 0:
            if game_state.board[r - 1][c - 1][0] == 'b':
                moves.append(Move((r, c), (r - 1, c - 1), game_state.board))
            elif (r - 1, c - 1) == game_state.en_passant_possible:
                moves.append(Move((r, c), (r - 1, c - 1), game_state.board, enpassant_possible=True))

        if c + 1 <= 7:
            if game_state.board[r - 1][c + 1][0] == 'b':
                moves.append(Move((r, c), (r - 1, c + 1), game_state.board))
            elif (r - 1, c + 1) == game_state.en_passant_possible:
                moves.append(Move((r, c), (r - 1, c + 1), game_state.board, enpassant_possible=True))
    else:
        if game_state.board[r + 1][c] == "--":  # one square pawn advance
            moves.append(Move((r, c), (r + 1, c), game_state.board))
            if r == 1 and game_state.board[r + 2][c] == "--":
                moves.append(Move((r, c), (r + 2, c), game_state.board))
        if c - 1 >= 0:
            if game_state.board[r + 1][c - 1][0] == 'w':
                moves.append(Move((r, c), (r + 1, c - 1), game_state.board))
            elif ((r + 1, c - 1) == game_state.en_passant_possible):
                moves.append(Move((r, c), (r + 1, c - 1), game_state.board, enpassant_possible=True))
        if c + 1 <= 7:
            if game_state.board[r + 1][c + 1][0] == 'w':
                moves.append(Move((r, c), (r + 1, c + 1), game_state.board))
            elif (r + 1, c + 1) == game_state.en_passant_possible:
                moves.append(Move((r, c), (r + 1, c + 1), game_state.board, enpassant_possible=True))
def get_rook_moves(game_state, r, c, moves):
    """
        Get all possible moves for a rook at the given position (r, c).

        Args:
            r (int): Row of the rook.
            c (int): Column of the rook.
            moves (list): List to store the generated moves.

        This method generates all possible moves for a rook at the specified position on the chessboard.
        It considers moves along the rows and columns until it encounters a piece or the edge of the board.
    """
    if game_state.white_to_move:
        for row in range(r-1, -1, -1):
            if game_state.board[row][c] == "--":
                moves.append(Move((r, c), (row, c), game_state.board))
            elif game_state.board[row][c][0] == 'b':
                moves.append(Move((r, c), (row, c), game_state.board))
                break
            else:
                break
        for row in range(r+1, 8):
            if game_state.board[row][c] == "--":
                moves.append(Move((r, c), (row, c), game_state.board))
            elif game_state.board[row][c][0] == 'b':
                moves.append(Move((r, c), (row, c), game_state.board))
                break
            else:
                break
        for col in range(c-1, -1, -1):
            if game_state.board[r][col] == "--":
                moves.append(Move((r, c), (r, col), game_state.board))
            elif game_state.board[r][col][0] == 'b':
                moves.append(Move((r, c), (r, col), game_state.board))
                break
            else:
                break
        for col in range(c+1, 8):
            if game_state.board[r][col] == "--":
                moves.append(Move((r, c), (r, col), game_state.board))
            elif game_state.board[r][col][0] == 'b':
                moves.append(Move((r, c), (r, col), game_state.board))
                break
            else:
                break
    else:
        for row in range(r-1, -1, -1):
            if game_state.board[row][c] == "--":
                moves.append(Move((r, c), (row, c), game_state.board))
            elif game_state.board[row][c][0] == 'w':
                moves.append(Move((r, c), (row, c), game_state.board))
                break
            else:
                break
        for row in range(r+1, 8):
            if game_state.board[row][c] == "--":
                moves.append(Move((r, c), (row, c), game_state.board))
            elif game_state.board[row][c][0] == 'w':
                moves.append(Move((r, c), (row, c), game_state.board))
                break
            else:
                break
        for col in range(c-1, -1, -1):
            if game_state.board[r][col] == "--":
                moves.append(Move((r, c), (r, col), game_state.board))
            elif game_state.board[r][col][0] == 'w':
                moves.append(Move((r, c), (r, col), game_state.board))
                break
            else:
                break
        for col in range(c+1, 8):
            if game_state.board[r][col] == "--":
                moves.append(Move((r, c), (r, col), game_state.board))
            elif game_state.board[r][col][0] == 'w':
                moves.append(Move((r, c), (r, col), game_state.board))
                break
            else:
                break

def get_knight_moves(game_state, r, c, moves):
    """
        Get all possible moves for a knight at the given position (r, c).

        Args:
            r (int): Row of the knight.
            c (int): Column of the knight.
            moves (list): List to store the generated moves.

        This method generates all possible moves for a knight at the specified position on the chessboard.
        It considers all eight possible knight moves, checking for validity and capturing opponent pieces.

        """
    if game_state.white_to_move:
        if r-2 >= 0 and c-1 >= 0:
            if game_state.board[r-2][c-1] == "--":
                moves.append(Move((r, c), (r-2, c-1), game_state.board))
            elif game_state.board[r-2][c-1][0] == 'b':
                moves.append(Move((r, c), (r-2, c-1), game_state.board))
        if r-2 >= 0 and c+1 <= 7:
            if game_state.board[r-2][c+1] == "--":
                moves.append(Move((r, c), (r-2, c+1), game_state.board))
            elif game_state.board[r-2][c+1][0] == 'b':
                moves.append(Move((r, c), (r-2, c+1), game_state.board))
        if r-1 >= 0 and c-2 >= 0:
            if game_state.board[r-1][c-2] == "--":
                moves.append(Move((r, c), (r-1, c-2), game_state.board))
            elif game_state.board[r-1][c-2][0] == 'b':
                moves.append(Move((r, c), (r-1, c-2), game_state.board))
        if r-1 >= 0 and c+2 <= 7:
            if game_state.board[r-1][c+2] == "--":
                moves.append(Move((r, c), (r-1, c+2), game_state.board))
            elif game_state.board[r-1][c+2][0] == 'b':
                moves.append(Move((r, c), (r-1, c+2), game_state.board))
        if r+1 <= 7 and c-2 >= 0:
            if game_state.board[r+1][c-2] == "--":
                moves.append(Move((r, c), (r+1, c-2), game_state.board))
            elif game_state.board[r+1][c-2][0] == 'b':
                moves.append(Move((r, c), (r+1, c-2), game_state.board))
        if r+1 <= 7 and c+2 <= 7:
            if game_state.board[r+1][c+2] == "--":
                moves.append(Move((r, c), (r+1, c+2), game_state.board))
            elif game_state.board[r+1][c+2][0] == 'b':
                moves.append(Move((r, c), (r+1, c+2), game_state.board))
        if r+2 <= 7 and c-1 >= 0:
            if game_state.board[r+2][c-1] == "--":
                moves.append(Move((r, c), (r+2, c-1), game_state.board))
            elif game_state.board[r+2][c-1][0] == 'b':
                moves.append(Move((r, c), (r+2, c-1), game_state.board))
        if r+2 <= 7 and c+1 <= 7:
            if game_state.board[r+2][c+1] == "--":
                moves.append(Move((r, c), (r+2, c+1), game_state.board))
            elif game_state.board[r+2][c+1][0] == 'b':
                moves.append(Move((r, c), (r+2, c+1), game_state.board))
    else:
        if r-2 >= 0 and c-1 >= 0:
            if game_state.board[r-2][c-1] == "--":
                moves.append(Move((r, c), (r-2, c-1), game_state.board))
            elif game_state.board[r-2][c-1][0] == 'w':
                moves.append(Move((r, c), (r-2, c-1), game_state.board))
        if r-2 >= 0 and c+1 <= 7:
            if game_state.board[r-2][c+1] == "--":
                moves.append(Move((r, c), (r-2, c+1), game_state.board))
            elif game_state.board[r-2][c+1][0] == 'w':
                moves.append(Move((r, c), (r-2, c+1), game_state.board))
        if r-1 >= 0 and c-2 >= 0:
            if game_state.board[r-1][c-2] == "--":
                moves.append(Move((r, c), (r-1, c-2), game_state.board))
            elif game_state.board[r-1][c-2][0] == 'w':
                moves.append(Move((r, c), (r-1, c-2), game_state.board))
        if r-1 >= 0 and c+2 <= 7:
            if game_state.board[r-1][c+2] == "--":
                moves.append(Move((r, c), (r-1, c+2), game_state.board))
            elif game_state.board[r-1][c+2][0] == 'w':
                moves.append(Move((r, c), (r-1, c+2), game_state.board))
        if r+1 <= 7 and c-2 >= 0:
            if game_state.board[r+1][c-2] == "--":
                moves.append(Move((r, c), (r+1, c-2), game_state.board))
            elif game_state.board[r+1][c-2][0] == 'w':
                moves.append(Move((r, c), (r+1, c-2), game_state.board))
        if r+1 <= 7 and c+2 <= 7:
            if game_state.board[r+1][c+2] == "--":
                moves.append(Move((r, c), (r+1, c+2), game_state.board))
            elif game_state.board[r+1][c+2][0] == 'w':
                moves.append(Move((r, c), (r+1, c+2), game_state.board))
        if r+2 <= 7 and c-1 >= 0:
            if game_state.board[r+2][c-1] == "--":
                moves.append(Move((r, c), (r+2, c-1), game_state.board))
            elif game_state.board[r+2][c-1][0] == 'w':
                moves.append(Move((r, c), (r+2, c-1), game_state.board))
        if r+2 <= 7 and c+1 <= 7:
            if game_state.board[r+2][c+1] == "--":
                moves.append(Move((r, c), (r+2, c+1), game_state.board))
            elif game_state.board[r+2][c+1][0] == 'w':
                moves.append(Move((r, c), (r+2, c+1), game_state.board))

def get_bishop_moves(game_state, r, c, moves):
    """
        Get all possible moves for a bishop at the given position (r, c).

        Args:
            r (int): Row of the bishop.
            c (int): Column of the bishop.
            moves (list): List to store the generated moves.

            This method generates all possible moves for a bishop at the specified position on the chessboard.
            It considers all diagonal moves, checking for validity and capturing opponent pieces.

    """
    if game_state.white_to_move:
        for i in range(1, 8):
            if r-i >= 0 and c-i >= 0:
                if game_state.board[r-i][c-i] == "--":
                    moves.append(Move((r, c), (r-i, c-i), game_state.board))
                elif game_state.board[r-i][c-i][0] == 'b':
                    moves.append(Move((r, c), (r-i, c-i), game_state.board))
                    break
                else:
                    break
        for i in range(1, 8):
            if r-i >= 0 and c+i <= 7:
                if game_state.board[r-i][c+i] == "--":
                    moves.append(Move((r, c), (r-i, c+i), game_state.board))
                elif game_state.board[r-i][c+i][0] == 'b':
                    moves.append(Move((r, c), (r-i, c+i), game_state.board))
                    break
                else:
                    break
        for i in range(1, 8):
            if r+i <= 7 and c-i >= 0:
                if game_state.board[r+i][c-i] == "--":
                    moves.append(Move((r, c), (r+i, c-i), game_state.board))
                elif game_state.board[r+i][c-i][0] == 'b':
                    moves.append(Move((r, c), (r+i, c-i), game_state.board))
                    break
                else:
                    break
        for i in range(1, 8):
            if r+i <= 7 and c+i <= 7:
                if game_state.board[r+i][c+i] == "--":
                    moves.append(Move((r, c), (r+i, c+i), game_state.board))
                elif game_state.board[r+i][c+i][0] == 'b':
                    moves.append(Move((r, c), (r+i, c+i), game_state.board))
                    break
                else:
                    break
    else:
        for i in range(1, 8):
            if r-i >= 0 and c-i >= 0:
                if game_state.board[r-i][c-i] == "--":
                    moves.append(Move((r, c), (r-i, c-i), game_state.board))
                elif game_state.board[r-i][c-i][0] == 'w':
                    moves.append(Move((r, c), (r-i, c-i), game_state.board))
                    break
                else:
                    break
        for i in range(1, 8):
            if r-i >= 0 and c+i <= 7:
                if game_state.board[r-i][c+i] == "--":
                    moves.append(Move((r, c), (r-i, c+i), game_state.board))
                elif game_state.board[r-i][c+i][0] == 'w':
                    moves.append(Move((r, c), (r-i, c+i), game_state.board))
                    break
                else:
                    break
        for i in range(1, 8):
            if r+i <= 7 and c-i >= 0:
                if game_state.board[r+i][c-i] == "--":
                    moves.append(Move((r, c), (r+i, c-i), game_state.board))
                elif game_state.board[r+i][c-i][0] == 'w':
                    moves.append(Move((r, c), (r+i, c-i), game_state.board))
                    break
                else:
                    break
        for i in range(1, 8):
            if r+i <= 7 and c+i <= 7:
                if game_state.board[r+i][c+i] == "--":
                    moves.append(Move((r, c), (r+i, c+i), game_state.board))
                elif game_state.board[r+i][c+i][0] == 'w':
                    moves.append(Move((r, c), (r+i, c+i), game_state.board))
                    break
                else:
                    break

def get_queen_moves(game_state, r, c, moves):
    """
    Get all possible moves for a queen at the given position (r, c).

    Args:
        r (int): Row of the queen.
        c (int): Column of the queen.
        moves (list): List to store the generated moves.

        This method generates all possible moves for a queen at the specified position on the chessboard.
        It combines the moves of a rook and a bishop, checking for validity and capturing opponent pieces.

    """
    game_state.get_rook_moves(r, c, moves)
    game_state.get_bishop_moves(r, c, moves)

def get_king_moves(game_state, r, c, moves):
    """
        Get all possible moves for a king at the given position (r, c).

        Args:
            r (int): Row of the king.
            c (int): Column of the king.
            moves (list): List to store the generated moves.

        This method generates all possible moves for a king at the specified position on the chessboard.
        It considers the king's possible moves in all directions, checking for validity and capturing opponent pieces.

    """
    if game_state.white_to_move:
        if r-1 >= 0:
            if game_state.board[r-1][c] == "--":
                moves.append(Move((r, c), (r-1, c), game_state.board))
            elif game_state.board[r-1][c][0] == 'b':
                moves.append(Move((r, c), (r-1, c), game_state.board))
        if r-1 >= 0 and c-1 >= 0:
            if game_state.board[r-1][c-1] == "--":
                moves.append(Move((r, c), (r-1, c-1), game_state.board))
            elif game_state.board[r-1][c-1][0] == 'b':
                moves.append(Move((r, c), (r-1, c-1), game_state.board))
        if r-1 >= 0 and c+1 <= 7:
            if game_state.board[r-1][c+1] == "--":
                moves.append(Move((r, c), (r-1, c+1), game_state.board))
            elif game_state.board[r-1][c+1][0] == 'b':
                moves.append(Move((r, c), (r-1, c+1), game_state.board))
        if c-1 >= 0:
            if game_state.board[r][c-1] == "--":
                moves.append(Move((r, c), (r, c-1), game_state.board))
            elif game_state.board[r][c-1][0] == 'b':
                moves.append(Move((r, c), (r, c-1), game_state.board))
        if c+1 <= 7:
            if game_state.board[r][c+1] == "--":
                moves.append(Move((r, c), (r, c+1), game_state.board))
            elif game_state.board[r][c+1][0] == 'b':
                moves.append(Move((r, c), (r, c+1), game_state.board))
        if r+1 <= 7:
            if game_state.board[r+1][c] == "--":
                moves.append(Move((r, c), (r+1, c), game_state.board))
            elif game_state.board[r+1][c][0] == 'b':
                moves.append(Move((r, c), (r+1, c), game_state.board))
        if r+1 <= 7 and c-1 >= 0:
            if game_state.board[r+1][c-1] == "--":
                moves.append(Move((r, c), (r+1, c-1), game_state.board))
            elif game_state.board[r+1][c-1][0] == 'b':
                moves.append(Move((r, c), (r+1, c-1), game_state.board))
        if r+1 <= 7 and c+1 <= 7:
            if game_state.board[r+1][c+1] == "--":
                moves.append(Move((r, c), (r+1, c+1), game_state.board))
            elif game_state.board[r+1][c+1][0] == 'b':
                moves.append(Move((r, c), (r+1, c+1), game_state.board))
    else:
        if r-1 >= 0:
            if game_state.board[r-1][c] == "--":
                moves.append(Move((r, c), (r-1, c), game_state.board))
            elif game_state.board[r-1][c][0] == 'w':
                moves.append(Move((r, c), (r-1, c), game_state.board))
        if r-1 >= 0 and c-1 >= 0:
            if game_state.board[r-1][c-1] == "--":
                moves.append(Move((r, c), (r-1, c-1), game_state.board))
            elif game_state.board[r-1][c-1][0] == 'w':
                moves.append(Move((r, c), (r-1, c-1), game_state.board))
        if r-1 >= 0 and c+1 <= 7:
            if game_state.board[r-1][c+1] == "--":
                moves.append(Move((r, c), (r-1, c+1), game_state.board))
            elif game_state.board[r-1][c+1][0] == 'w':
                moves.append(Move((r, c), (r-1, c+1), game_state.board))
        if c-1 >= 0:
            if game_state.board[r][c-1] == "--":
                moves.append(Move((r, c), (r, c-1), game_state.board))
            elif game_state.board[r][c-1][0] == 'w':
                moves.append(Move((r, c), (r, c-1), game_state.board))
        if c+1 <= 7:
            if game_state.board[r][c+1] == "--":
                moves.append(Move((r, c), (r, c+1), game_state.board))
            elif game_state.board[r][c+1][0] == 'w':
                moves.append(Move((r, c), (r, c+1), game_state.board))
        if r+1 <= 7:
            if game_state.board[r+1][c] == "--":
                moves.append(Move((r, c), (r+1, c), game_state.board))
            elif game_state.board[r+1][c][0] == 'w':
                moves.append(Move((r, c), (r+1, c), game_state.board))
        if r+1 <= 7 and c-1 >= 0:
            if game_state.board[r+1][c-1] == "--":
                moves.append(Move((r, c), (r+1, c-1), game_state.board))
            elif game_state.board[r+1][c-1][0] == 'w':
                moves.append(Move((r, c), (r+1, c-1), game_state.board))
        if r+1 <= 7 and c+1 <= 7:
            if game_state.board[r+1][c+1] == "--":
                moves.append(Move((r, c), (r+1, c+1), game_state.board))
            elif game_state.board[r+1][c+1][0] == 'w':
                moves.append(Move((r, c), (r+1, c+1), game_state.board))

def random_move(valid_moves):
    return valid_moves[random.randint(0, len(valid_moves) - 1)]
