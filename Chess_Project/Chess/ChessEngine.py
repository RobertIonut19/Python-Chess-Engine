"""
The GameState() class is responsible for storing all the information about the current state of a chess game.
It is responsible for checking if a move made by the user is valid and updating the board accordingly.
It records all the moves made so far.
"""

import copy as c

class Move():
    pass

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

        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                                'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkMate = False
        self.staleMate = False
        self.en_passant_possible = () #coordinates for the square where en-passant capture is possible

        self.currentCastlingRights = Castle_rights(True, True, True, True)
        self.castleRightsLog = [Castle_rights(self.currentCastlingRights.wks, self.currentCastlingRights.bks,
                                                self.currentCastlingRights.wqs, self.currentCastlingRights.bqs)]

    def makeMove(self, move):
        '''
        Takes a move as a parameter and executes it (this will not work for castling, pawn promotion and en-passant)
        '''
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.moveLog.append(move) #for undo / history of the game
        self.whiteToMove = not self.whiteToMove #swap players

        if move.piece_moved == 'wK':
            self.whiteKingLocation = (move.end_row, move.end_col)
        elif move.piece_moved == 'bK':
            self.blackKingLocation = (move.end_row, move.end_col)

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
        self.castleRightsLog.append(Castle_rights(self.currentCastlingRights.wks, self.currentCastlingRights.bks,
                                                    self.currentCastlingRights.wqs, self.currentCastlingRights.bqs))

    def undoMove(self):
        '''
        Undo the last move made
        '''
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.whiteToMove = not self.whiteToMove
            if move.piece_moved == 'wK':
                self.whiteKingLocation = (move.start_row, move.start_col)
            elif move.piece_moved == 'bK':
                self.blackKingLocation = (move.start_row, move.start_col)

        if move.is_en_passant_move:
            self.board[move.end_row][move.end_col] = "--"
            self.board[move.start_row][move.end_col] = move.piece_captured
            self.en_passant_possible = (move.end_row, move.end_col)

        if move.piece_moved[1] == 'p' and abs(move.start_row - move.end_row) == 2:
            self.en_passant_possible = ()

        self.castleRightsLog.pop() #remove the last castle rights from the log
        new_rights = c.deepcopy(self.castleRightsLog[-1])
        self.currentCastlingRights = new_rights

        if move.is_castle_move:
            if move.end_col - move.start_col == 2: #kingside
                self.board[move.end_row][move.end_col+1] = self.board[move.end_row][move.end_col-1]
                self.board[move.end_row][move.end_col-1] = "--"
            else: #queenside
                self.board[move.end_row][move.end_col-2] = self.board[move.end_row][move.end_col+1]
                self.board[move.end_row][move.end_col+1] = "--"



    def update_castle_rights(self, move):
        if move.piece_moved == 'wK':
            self.currentCastlingRights.wks = False
            self.currentCastlingRights.wqs = False
        elif move.piece_moved == 'bK':
            self.currentCastlingRights.bks = False
            self.currentCastlingRights.bqs = False
        elif move.piece_moved == 'wR':
            if move.start_row == 7:
                if move.start_col == 0:
                    self.currentCastlingRights.wqs = False
                elif move.start_col == 7:
                    self.currentCastlingRights.wks = False
        elif move.piece_moved == 'bR':
            if move.start_row == 0:
                if move.start_col == 0:
                    self.currentCastlingRights.bqs = False
                elif move.start_col == 7:
                    self.currentCastlingRights.bks = False

        # if a rook is captured
        if move.piece_captured == 'wR':
            if move.end_row == 7:
                if move.end_col == 0:
                    self.currentCastlingRights.wqs = False
                elif move.end_col == 7:
                    self.currentCastlingRights.wks = False
        elif move.piece_captured == 'bR':
            if move.end_row == 0:
                if move.end_col == 0:
                    self.currentCastlingRights.bqs = False
                elif move.end_col == 7:
                    self.currentCastlingRights.bks = False


    def getValidMoves(self):
        '''
        All moves considering checks
        '''

        for log in self.castleRightsLog:
            print(log.wks, log.wqs, log.bks, log.bqs)
        print()

        temp_en_passant_possible = self.en_passant_possible
        temp_castle_rights = Castle_rights(self.currentCastlingRights.wks, self.currentCastlingRights.bks,
                                            self.currentCastlingRights.wqs, self.currentCastlingRights.bqs)
        moves = self.getAllPossibleMoves()
        if self.whiteToMove:
            self.get_castle_moves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves)
        else:
            self.get_castle_moves(self.blackKingLocation[0], self.blackKingLocation[1], moves)

        for i in range(len(moves)-1, -1, -1):
            self.makeMove(moves[i])
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        if len(moves) == 0:
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False

        self.en_passant_possible = temp_en_passant_possible
        self.currentCastlingRights = temp_castle_rights
        return moves

    def inCheck(self):
        '''
        Determine if the current player is in check
        '''
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    def squareUnderAttack(self, r, c):
        '''
        Determine if the enemy can attack the square r, c
        '''
        self.whiteToMove = not self.whiteToMove
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        for move in oppMoves:
            if move.end_row == r and move.end_col == c:
                return True
        return False


    def getAllPossibleMoves(self):
        '''
        All moves without considering checks
        '''
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0] #get the color of the piece - w or b
                if (turn == 'w' and self.whiteToMove ) or (turn == 'b' and not self.whiteToMove): #verifica later on
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves) #call the appropriate move function based on piece type
        return moves

    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:
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


    def getRookMoves(self, r, c, moves):
        if self.whiteToMove:
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


    def getKnightMoves(self, r, c, moves):
        if self.whiteToMove:
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

    def getBishopMoves(self, r, c, moves):
        if self.whiteToMove:
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

    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

    def getKingMoves(self, r, c, moves):
        if self.whiteToMove:
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
        if self.squareUnderAttack(r, c):
            return
        if (self.whiteToMove and self.currentCastlingRights.wks) or (not self.whiteToMove and self.currentCastlingRights.bks):
            self.get_king_side_castle_moves(r, c, moves)
        if (self.whiteToMove and self.currentCastlingRights.wqs) or (not self.whiteToMove and self.currentCastlingRights.bqs):
            self.get_queen_side_castle_moves(r, c, moves)

    def get_king_side_castle_moves(self, r, c, moves):
        if self.board[r][c+1] == '--' and self.board[r][c+2] == '--':
            if not self.squareUnderAttack(r, c+1) and not self.squareUnderAttack(r, c+2):
                moves.append(Move((r, c), (r, c+2), self.board, is_castle_move=True))

    def get_queen_side_castle_moves(self, r, c, moves):
        if self.board[r][c-1] == '--' and self.board[r][c-2] == '--' and self.board[r][c-3] == '--':
            if not self.squareUnderAttack(r, c-1) and not self.squareUnderAttack(r, c-2):
                moves.append(Move((r, c), (r, c-2), self.board, is_castle_move=True))

class Castle_rights():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs


class Move():
            # use chess notation
            ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4,
                             "5": 3, "6": 2, "7": 1, "8": 0}
            rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}  # reverse the dictionary

            files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3,
                             "e": 4, "f": 5, "g": 6, "h": 7}
            cols_to_files = {v: k for k, v in files_to_cols.items()}  # reverse the dictionary

            def __init__(self, start_square, end_square, board, enpassant_possible=False, is_castle_move=False):
                self.start_row = start_square[0]
                self.start_col = start_square[1]
                self.end_row = end_square[0]
                self.end_col = end_square[1]

                self.piece_moved = board[self.start_row][self.start_col]
                self.piece_captured = board[self.end_row][self.end_col]

                self.moveId = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col

                self.is_pawn_promotion = False
                if (self.piece_moved == 'wp' and self.end_row == 0) or (self.piece_moved == 'bp' and self.end_row == 7):
                    self.is_pawn_promotion = True

                self.is_en_passant_move = enpassant_possible
                if self.is_en_passant_move:
                    self.piece_captured = 'wp' if self.piece_moved == 'bp' else 'bp'

                self.is_castle_move = is_castle_move


            def __eq__(self, other):
                '''
                Overriding the equals method
                '''
                if isinstance(other, Move):
                    # return self.start_row == other.start_row and self.start_col == other.start_col and self.end_row == other.end_row and self.end_col == other.end_col
                    return self.moveId == other.moveId
                return False

            def get_chess_notation(self):
                return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row,
                                                                                               self.end_col)

            def get_rank_file(self, row, col):
                return self.cols_to_files[col] + self.rows_to_ranks[row]
