# storing information about the state of the chess game and determening the valid moves # 
from typing import no_type_check_decorator
import numpy as np


class GameState(): 
    def __init__(self):
        # 8x8 List to represent board
        # each field contains of two characters: player and piece
        self.board = [
            ["bR","bN", "bB", "bQ", "bK", "bB","bN", "bR"],
            ["bP","bP", "bP", "bP", "bP", "bP","bP", "bP"],
            ["--","--", "--", "--", "--", "--","--", "--"],
            ["--","--", "--", "--", "--", "--","--", "--"],
            ["--","--", "--", "--", "--", "--","--", "--"],
            ["--","--", "--", "--", "--", "--","--", "--"],
            ["wP","wP", "wP", "wP", "wP", "wP","wP", "wP"],
            ["wR","wN", "wB", "wQ", "wK", "wB","wN", "wR"]
        ]
        # self.board = [
        #     ["bR","bN", "bB", "--", "bK", "bB","bN", "bR"],
        #     ["bP","bP", "bP", "bP", "--", "bP","bP", "bP"],
        #     ["--","--", "--", "--", "--", "--","--", "--"],
        #     ["--","--", "--", "--", "bQ", "--","--", "--"],
        #     ["--","--", "--", "--", "--", "--","--", "--"],
        #     ["--","--", "--", "--", "--", "--","--", "--"],
        #     ["wP","wP", "wP", "wP", "wQ", "wP","wP", "wP"],
        #     ["wR","wN", "wB", "--", "wK", "wB","wN", "wR"]
        # ]
        # self.board = [
        #     ["--","--", "--", "--", "--", "--","--", "--"],
        #     ["--","--", "--", "--", "--", "--","--", "--"],
        #     ["--","--", "--", "--", "--", "--","--", "--"],
        #     ["--","--", "--", "--", "--", "--","--", "--"],
        #     ["--","--", "--", "--", "--", "--","--", "--"],
        #     ["--","wK", "--", "--", "--", "--","--", "--"],
        #     ["--","--", "--", "wQ", "--", "--","--", "--"],
        #     ["--","bK", "--", "--", "--", "--","--", "--"]
        # ]
        self.whiteToMove = True
        self.moveLog = []
        self.moveFunctions = {'P': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getNightMoves, 'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}
        self.whiteKingPosition = (7,4)
        self.blackKingPosition = (0,4)
        # self.whiteKingPosition = (5,1)
        # self.blackKingPosition = (7,1)
        # self.whiteQueenPosition = (7,3)
        # self.blackQueenPosition = (0,3)
        self.checkMate = False
        self.staleMate = False
        self.inCheck = False
        # self.whiteInCheck = False
        # self.blackInCheck = False
        # self.whiteQueenUnderAttack = False
        # self.blackQueenUnderAttack = False
        self.pins = []
        self.checks = []
        self.possibleEnPassantSquare = ()
        self.enPassantPossibleLog = [self.possibleEnPassantSquare]
        # self.currentCastlingRights = CastleRights(True, True, True, True)
        self.currentCastlingRights = CastleRights(False, False, False, False)
        self.castleRightsLog = [ CastleRights(self.currentCastlingRights.whiteKingCastle, self.currentCastlingRights.whiteQueenCastle, self.currentCastlingRights.blackKingCastle, self.currentCastlingRights.blackQueenCastle)]
        self.lateGameWeight = 1
        # self.lastPieceMovedWhite = None
        # self.lastPieceMovedBlack = None
        # self.lastMovedPiecesWhite = []
        # self.lastMovedPiecesBlack = []

    # moves pieces on board except casteling, en-passant and pawn capture
    def makeMove(self, move):
        # reset checks as makeMove must break check to be called
        # self.blackInCheck = False
        # self.whiteInCheck = False
        # self.whiteQueenUnderAttack = False
        # self.blackQueenUnderAttack = False
        # makes the move
        self.board[move.startSquare[0]][move.startSquare[1]] = "--"
        self.board[move.endSquare[0]][move.endSquare[1]] = move.pieceMoved
        self.moveLog.append(move) # log to be able to undo moves        
        # if self.whiteToMove:
        #     self.lastMovedPiecesWhite.append((move.endSquare))
        # else:
        #     self.lastMovedPiecesBlack.append((move.endSquare))
        # checks opponents king
        # if move.isCheckMove:
        #     if move.pieceMoved[0] == 'w':
        #         self.blackInCheck = True
        #     elif move.pieceMoved[0] == 'b': 
        #         self.whiteInCheck = True
        # if move.attacksQueen:
        #     if move.pieceMoved[0] == 'w':
        #         self.blackQueenUnderAttack = False
        #     elif move.pieceMoved[0] == 'b': 
        #         self.whiteQueenUnderAttack = False
        self.whiteToMove = not self.whiteToMove # players take turns        
        if move.pieceMoved == "wK" or move.pieceMoved == "bK": # TODO make more efficient
            self.updateKingPosition(move)
        if move.pieceMoved == "wQ" or move.pieceMoved == "bQ": 
            self.updateQueenPosition(move)
        # pawn promotion
        if move.isPawnPromotion:
            self.board[move.endSquare[0]][move.endSquare[1]] = move.pieceMoved[0] + 'Q'
        # en passant
        if move.isEnPassantMove:
            self.board[move.startSquare[0]][move.endSquare[1]] = "--" # capturing the pawn
        if move.pieceMoved[1] == 'P' and abs(move.startSquare[0] - move.endSquare[0]) == 2: # declare possible en passant move
            self.possibleEnPassantSquare = ((move.startSquare[0] + move.endSquare[0]) // 2, move.startSquare[1])
        else: 
            self.possibleEnPassantSquare = ()
        self.enPassantPossibleLog.append(self.possibleEnPassantSquare)
        # castling
        if move.isCastleMove:
            if  move.endSquare[1] - move.startSquare[1] == 2: # Kingside castling
                self.board[move.startSquare[0]][move.endSquare[1] - 1] = self.board[move.startSquare[0]][move.endSquare[1] + 1] # copies the rook
                self.board[move.startSquare[0]][move.endSquare[1] + 1] = "--" # removes the rook
            else: # queen side castling
                self.board[move.startSquare[0]][move.endSquare[1] + 1] = self.board[move.startSquare[0]][move.endSquare[1] - 2] # copies the rook
                self.board[move.startSquare[0]][move.endSquare[1] - 2] = "--" # removes the rook
        self.updateCastleRights(move)
        self.castleRightsLog.append(CastleRights(self.currentCastlingRights.whiteKingCastle, self.currentCastlingRights.whiteQueenCastle, self.currentCastlingRights.blackKingCastle, self.currentCastlingRights.blackQueenCastle))
        

             

    def undoMove(self):
        if len(self.moveLog)>0:
            move = self.moveLog.pop()
            self.board[move.startSquare[0]][move.startSquare[1]] = move.pieceMoved
            self.board[move.endSquare[0]][move.endSquare[1]] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            if move.pieceMoved == "wK" or move.pieceMoved == "bK":
                self.reverseKingPosition(move)
            # if self.whiteToMove:
            #     self.lastMovedPiecesWhite.pop()
            # else:
            #     self.lastMovedPiecesBlack.pop()
            # if move.pieceMoved == "wQ" or move.pieceMoved == "bQ":
            #     self.reverseQueenPosition(move)
            # undo en passant
            if move.isEnPassantMove:
                self.board[move.endSquare[0]][move.endSquare[1]] = "--" # leave landing square blank
                self.board[move.startSquare[0]][move.endSquare[1]] = move.pieceCaptured
            self.enPassantPossibleLog.pop()
            self.possibleEnPassantSquare = self.enPassantPossibleLog[-1]
                
            # undo castling rights
            self.castleRightsLog.pop()
            self.currentCastlingRights = CastleRights(self.castleRightsLog[-1].whiteKingCastle, self.castleRightsLog[-1].whiteQueenCastle, self.castleRightsLog[-1].blackKingCastle, self.castleRightsLog[-1].blackQueenCastle)
            # undo castling move
            if move.isCastleMove:
                if  move.endSquare[1] - move.startSquare[1] == 2: # Kingside castling
                    self.board[move.startSquare[0]][move.endSquare[1] + 1] = self.board[move.startSquare[0]][move.endSquare[1] - 1] # copies the rook
                    self.board[move.startSquare[0]][move.endSquare[1] - 1] = "--" # removes the rook
                else: # queen side castling
                    self.board[move.startSquare[0]][move.endSquare[1] - 2] = self.board[move.startSquare[0]][move.endSquare[1] + 1] # copies the rook
                    self.board[move.startSquare[0]][move.endSquare[1] + 1] = "--" # removes the rook
            self.checkMate = False
            self.staleMate = False
            # undo check status
            # checks opponents king
            # if move.isCheckMove:
            #     if move.pieceMoved[0] == 'w':
            #         self.blackInCheck = False
            #     elif move.pieceMoved[0] == 'b': 
            #         self.whiteInCheck = False
            # if move.attacksQueen:
            #     if move.pieceMoved[0] == 'w':
            #         self.blackQueenUnderAttack = False
            #     elif move.pieceMoved[0] == 'b': 
            #         self.whiteQueenUnderAttack = False

    # possible moves without considering check
    def getPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                player = self.board[r][c][0]
                if (player == 'w' and self.whiteToMove) or (player == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]                    
                    self.moveFunctions[piece](r,c,moves) # calls appropriate move function
        return moves

    # possible moves considering check
    def getValidMoves(self):
        moves = []
        self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()
        if self.whiteToMove:
            kingRow = self.whiteKingPosition[0]
            kingCol = self.whiteKingPosition[1]
        else:
            kingRow = self.blackKingPosition[0]
            kingCol = self.blackKingPosition[1]
        if self.inCheck:
            if len(self.checks) == 1: # block or king escape possible
                moves = self.getPossibleMoves()
                # blocking the check
                check = self.checks[0]
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol]
                validSquares = []
                if pieceChecking[1] == 'N':
                    # night can be captured to break check
                    validSquares = [(checkRow, checkCol)]
                else:
                    for i in range(1,8):
                        validSquare = (kingRow + check[2] * i, kingCol + check[3] * i) # adds direction vector
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[1] == checkCol:
                            break
                # get rid of invalid moves
                for i in range(len(moves) -1, -1, -1):
                    if moves[i].pieceMoved[1] != 'K': # king doesnt dodge the attack
                        if not (moves[i].endSquare[0], moves[i].endSquare[1]) in validSquares:
                            moves.remove(moves[i])
            else: # 2 checks -> king needs to move
                self.getKingMoves(kingRow, kingCol, moves)
        else: # no check
            moves = self.getPossibleMoves()
            if self.whiteToMove:
                self.getCastleMoves(self.whiteKingPosition[0], self.whiteKingPosition[1], moves)
            else:
                self.getCastleMoves(self.blackKingPosition[0], self.blackKingPosition[1], moves)            

        # check if moves deliver check to opponents king
        # for move in moves:
        #     if self.moveDeliversCheck(move):
        #         move.isCheckMove = True
        #     if self.moveAttacksQueen(move):
        #         move.attacksQueen = True

        # check for end of game
        if len(moves) == 0:
            if self.inCheck:
                self.checkMate = True
            else:
                self.staleMate = True
        return moves


    def checkForPinsAndChecks(self):
        pins = []
        checks = []
        inCheck = False
        if self.whiteToMove:
            enemyColor = 'b'
            allyColor = 'w'
            startRow = self.whiteKingPosition[0]
            startCol = self.whiteKingPosition[1]
        else:
            enemyColor = 'w'
            allyColor = 'b'
            startRow = self.blackKingPosition[0]
            startCol = self.blackKingPosition[1]
        directions = ((-1,0), (0,-1), (1,0), (0,1), (-1,-1), (-1, 1), (1, -1), (1,1))
        for j in range(len(directions)):
            d = directions[j]
            possiblePin = () # reset pins
            for i in range(1,8):
                endRow = startRow + d[0] * i
                endCol = startCol + d[1] * i
                if 0 <= endCol < 8 and 0 <= endRow < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allyColor and endPiece[1] != 'K':
                        if possiblePin == ():
                            possiblePin = (endRow, endCol, d[0], d[1])
                        else:
                            break
                    elif endPiece[0] == enemyColor:
                        type = endPiece[1]
                        if (0 <= j <= 3 and type == 'R') or (4 <= j <= 7 and type == 'B') or (i == 1 and type== 'P' and ((enemyColor == 'w' and 6 <= j <= 7) or (enemyColor == 'b' and 4 <= j <= 5))) or type == 'Q' or (i == 1 and type == 'K'):
                            if possiblePin == (): # check cuz no piece blocks
                                inCheck = True
                                checks.append((endRow, endCol, d[0], d[1]))
                                break
                            else: # a piece is blocking -> pin
                                pins.append(possiblePin)
                                break
                        else: # no check
                            break 
                else: # off board
                    break #
        # check for night checks
        knightMoves = ((-2,1),(2,-1), (2,1),(-2,-1), (1,2), (-1,2), (-1,-2), (1,-2)) 
        for m in knightMoves:
            endrow = startRow + m[0]
            endcol = startCol + m[1]
            if 0 <= endrow < 8 and 0 <= endcol < 8:
                endPiece = self.board[endrow][endcol]
                if endPiece[0] == enemyColor and endPiece[1] == 'N':
                    inCheck = True
                    checks.append((endrow, endcol, m[0], m[1]))
        return inCheck, pins, checks

    # determines if a certain fiel is under attack
    def squareUnderAttack(self, r, c):
        underAttack = False
        if self.whiteToMove:
            enemyColor = 'b'
            allyColor = 'w'
        else:
            enemyColor = 'w'
            allyColor = 'b'
        startRow = r
        startCol = c
        directions = ((-1,0), (0,-1), (1,0), (0,1), (-1,-1), (-1, 1), (1, -1), (1,1))
        for j in range(len(directions)):
            d = directions[j]
            possiblePin = () # reset pins
            for i in range(1,8):
                endRow = startRow + d[0] * i
                endCol = startCol + d[1] * i
                if 0 <= endCol < 8 and 0 <= endRow < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allyColor and endPiece[1] != 'K': # phantom king shouldnt block
                        if possiblePin == ():
                            possiblePin = (endRow, endCol, d[0], d[1])
                        else:
                            break
                    elif endPiece[0] == enemyColor:
                        type = endPiece[1]
                        if (0 <= j <= 3 and type == 'R') or (4 <= j <= 7 and type == 'B') or (i == 1 and type== 'P' and ((enemyColor == 'w' and 6 <= j <= 7) or (enemyColor == 'b' and 4 <= j <= 5))) or type == 'Q' or (i == 1 and type == 'K'):
                            if possiblePin == (): # underAttack cuz no piece blocks
                                underAttack = True
                                break
                            else: # a piece is blocking 
                                break
                        else: # not underAttack
                            break 
                else: # off board
                    break #
        # check for night checks
        knightMoves = ((-2,1),(2,-1), (2,1),(-2,-1), (1,2), (-1,2), (-1,-2), (1,-2)) 
        for m in knightMoves:
            endrow = startRow + m[0]
            endcol = startCol + m[1]
            if 0 <= endrow < 8 and 0 <= endcol < 8:
                endPiece = self.board[endrow][endcol]
                if endPiece[0] == enemyColor and endPiece[1] == 'N':
                    underAttack = True
        return underAttack
        

    def updateKingPosition(self, move):
        if move.pieceMoved == "wK":
            self.whiteKingPosition = (move.endSquare[0], move.endSquare[1])
        elif move.pieceMoved == "bK":
            self.blackKingPosition = (move.endSquare[0], move.endSquare[1])

    def updateQueenPosition(self, move):
        if move.pieceMoved == "wQ":
            self.whiteQueenPosition = (move.endSquare[0], move.endSquare[1])
        elif move.pieceMoved == "bQ":
            self.blackQueenPosition = (move.endSquare[0], move.endSquare[1])

    def reverseKingPosition(self, move):
        if move.pieceMoved == "wK":
            self.whiteKingPosition = (move.startSquare[0], move.startSquare[1])
        if move.pieceMoved == "bK":
            self.blackKingPosition = (move.startSquare[0], move.startSquare[1])

    def reverseQueenPosition(self, move):
        if move.pieceMoved == "wQ":
            self.whiteQueenPosition = (move.startSquare[0], move.startSquare[1])
        if move.pieceMoved == "bQ":
            self.blackQueenPosition = (move.startSquare[0], move.startSquare[1])

    # update castle rights if king or rook move
    def updateCastleRights(self, move):
        # king moved
        if move.pieceMoved == "wK":
            self.currentCastlingRights.whiteKingCastle = False
            self.currentCastlingRights.whiteQueenCastle = False
        elif move.pieceMoved == "bK":
            self.currentCastlingRights.blackKingCastle = False
            self.currentCastlingRights.blackQueenCastle = False
        # rook getting moved
        elif move.pieceMoved == "wR":
            if move.startSquare[0] ==7:
                if move.startSquare[1] == 0:
                    self.currentCastlingRights.whiteQueenCastle = False
                elif move.startSquare[1] == 7:
                    self.currentCastlingRights.whiteKingCastle = False
        elif move.pieceMoved == "bR":
            if move.startSquare[0] ==0:
                if move.startSquare[1] == 0:
                    self.currentCastlingRights.blackQueenCastle = False
                elif move.startSquare[1] == 7:
                    self.currentCastlingRights.blackKingCastle = False
        # rook getting captured
        elif move.pieceCaptured == "wR":
            if move.endSquare[1] == 0:
                self.currentCastlingRights.whiteQueenCastle = False
            elif move.endSquare[1] == 7:
                self.currentCastlingRights.whiteKingCastle = False
        elif move.pieceCaptured == "bR":
            if move.endSquare[1] == 0:
                self.currentCastlingRights.blackQueenCastle = False
            elif move.endSquare[1] == 7:
                self.currentCastlingRights.blackKingCastle = False

            
    # generates possible moves for Pawns
    def getPawnMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1): # sees if piece is pinned
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])

        if self.whiteToMove:
            moveAmount = -1
            startRow = 6
            enemyColor = 'b'
            kingRow, kingCol = self.whiteKingPosition
        else: 
            moveAmount = 1
            startRow = 1
            enemyColor = 'w'
            kingRow, kingCol = self.blackKingPosition
 

        if self.board[r + moveAmount][c] == "--": # pawn moves 1 field
            if not piecePinned or pinDirection == (moveAmount, 0):
                moves.append(Move((r,c), (r + moveAmount,c), self.board))
                if r == startRow and self.board[startRow + moveAmount * 2][c] == "--": # pawn moves 2 fields
                    moves.append(Move((r,c), (r + moveAmount * 2,c), self.board))
        if c+1 <= 7:
            if not piecePinned or pinDirection == (moveAmount, 1):
                if self.board[r + moveAmount][c + 1][0] == enemyColor: # enemy piece
                    moves.append(Move((r,c), (r + moveAmount,c +1), self.board))
                elif (r-1,c +1) == self.possibleEnPassantSquare: # en passant
                    attackingPiece = blockingPiece = False
                    if kingRow == r:
                        if kingCol < c: # king to the left of the pawn
                            insideRange = range(kingCol + 1, c)
                            outsideRange = range(c + 2, 8)
                        else:   # king to the right of the pawn
                            insideRange = range(kingCol - 1, c + 1, -1)
                            outsideRange = range(c - 1, -1, -1)
                        for i in insideRange:
                            if self.board[r][i] != "--": # blocking piece in the way
                                blockingPiece = True
                        for i in outsideRange:
                            square = self.board[r][i]
                            if square[0] == enemyColor and (square[1] == 'R' or square[1] == 'Q'):
                                attackingPiece = True
                            elif square != "--":
                                blockingPiece = True
                    if not attackingPiece or blockingPiece:
                        moves.append(Move((r,c), (r + moveAmount,c +1), self.board, isEnPassantMove = True))
        if c-1 >= 0:
            if not piecePinned or pinDirection == (moveAmount, -1):
                if self.board[r + moveAmount][c - 1][0] == enemyColor: # enemy piece
                    moves.append(Move((r,c), (r + moveAmount,c -1), self.board))
                elif (r-1,c -1) == self.possibleEnPassantSquare: # en passant
                    attackingPiece = blockingPiece = False
                    if kingRow == r:
                        if kingCol < c: # king to the left of the pawn
                            insideRange = range(kingCol + 1, c - 1)
                            outsideRange = range(c + 1, 8)
                        else:   # king to the right of the pawn
                            insideRange = range(kingCol - 1, c , -1)
                            outsideRange = range(c - 2, -1, -1)
                        for i in insideRange:
                            if self.board[r][i] != "--": # blocking piece in the way
                                blockingPiece = True
                        for i in outsideRange:
                            square = self.board[r][i]
                            if square[0] == enemyColor and (square[1] == 'R' or square[1] == 'Q'):
                                attackingPiece = True
                            elif square != "--":
                                blockingPiece = True
                    if not attackingPiece or blockingPiece:
                        moves.append(Move((r,c), (r + moveAmount,c - 1), self.board, isEnPassantMove = True))

    # generates possible moves for Rooks
    def getRookMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1): # sees if piece is pinned
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                # if self.board[r][c][1] != 'Q': 
                #     self.pins.remove(self.pins[i])
                break
        directions = ((-1, 0), (0,-1), (1, 0), (0, 1))
        enemyColor = "b" if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1,8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endCol < 8 and 0 <= endRow < 8:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":
                            moves.append(Move((r,c), (endRow,endCol), self.board))
                        elif endPiece[0] == enemyColor:
                            moves.append(Move((r,c), (endRow,endCol), self.board))
                            break
                        else: # allied piece
                            break
                else: # off board
                    break


    # generates possible moves for Nights
    def getNightMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1): # sees if piece is pinned
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        allyColor = 'w' if self.whiteToMove else 'b'
        knightMoves = ((-2,1),(2,-1), (2,1),(-2,-1), (1,2), (-1,2), (-1,-2), (1,-2)) 
        for move in knightMoves:
            endrow = r + move[0]
            endcol = c + move[1]
            if 0 <= endrow < 8 and 0 <= endcol < 8:
                if not piecePinned:
                    endpiece = self.board[endrow][endcol]
                    if endpiece[0] != allyColor:
                        moves.append(Move((r,c), (endrow,endcol), self.board))

    # generates possible moves for Bishops
    def getBishopMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1): # sees if piece is pinned
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                if self.board[r][c][1] != 'Q': 
                    self.pins.remove(self.pins[i])
                break
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemyColor = "b" if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1,8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endCol < 8 and 0 <= endRow < 8:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":
                            moves.append(Move((r,c), (endRow,endCol), self.board))
                        elif endPiece[0] == enemyColor:
                            moves.append(Move((r,c), (endRow,endCol), self.board))
                            break
                        else: # allied piece
                            break
                else: # off board
                    break

    # generates possible moves for Queens
    def getQueenMoves(self, r, c, moves):
        self.getBishopMoves(r, c, moves)
        self.getRookMoves(r, c, moves)

    # generates possible moves for Kings
    def getKingMoves(self, r, c, moves):
        rowMoves = (-1,-1,-1,0,0,1,1,1)
        colMoves = (-1,0,1,-1,1,-1,0,1)
        allyColor = 'w' if self.whiteToMove else 'b'
        for i in range(8):
            endRow = r + rowMoves[i]
            endCol = c + colMoves[i]
            if 0 <= endCol < 8 and 0 <= endRow < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor: # not ally piece
                    # place king and check for checks
                    if allyColor == 'w':
                        self.whiteKingPosition = (endRow, endCol)
                    else:
                        self.blackKingPosition = (endRow, endCol)
                    inCheck, pins, checks = self.checkForPinsAndChecks()
                    if not inCheck:
                        moves.append(Move((r,c), (endRow,endCol), self.board))
                    # put king back
                    if allyColor == 'w':
                        self.whiteKingPosition = (r,c)
                    else:
                        self.blackKingPosition = (r,c)


    def getCastleMoves(self, r, c, moves):
        if self.squareUnderAttack(r, c):
            return
        if (self.whiteToMove and self.currentCastlingRights.whiteKingCastle) or (not self.whiteToMove and self.currentCastlingRights.blackKingCastle):
            self.getKingSideCastleMoves(r, c, moves)
        if (self.whiteToMove and self.currentCastlingRights.whiteQueenCastle) or (not self.whiteToMove and self.currentCastlingRights.blackQueenCastle):
            self.getQueenSideCastleMoves(r, c, moves)
        
    def getKingSideCastleMoves(self, r, c, moves):
        if self.board[r][c+1] == "--" and self.board[r][c+2] == "--":
            if not self.squareUnderAttack(r,c+1) and not self.squareUnderAttack(r,c+2):
                moves.append(Move((r,c), (r,c+2), self.board, isCastleMove = True))


    def getQueenSideCastleMoves(self, r, c, moves):
        if self.board[r][c-1] == "--" and self.board[r][c-2] == "--" and self.board[r][c-3] == "--":
            if not self.squareUnderAttack(r,c-1) and not self.squareUnderAttack(r,c-2):
                moves.append(Move((r,c), (r,c-2), self.board, isCastleMove = True))

    # TODO check for stalemate when material is low

    # TODO check for stalemate through move repetition

    # def moveDeliversCheck(self, move):
    #     self.makeMove(move)
    #     #check for a check
    #     if self.whiteToMove:
    #         if self.squareUnderAttack(self.whiteKingPosition[0], self.whiteKingPosition[1]):            
    #                 self.undoMove()
    #                 return True
    #     elif not self.whiteToMove:
    #         if self.squareUnderAttack(self.blackKingPosition[0], self.blackKingPosition[1]):            
    #                 self.undoMove()
    #                 return True
    #     self.undoMove()
    #     return False

    # def moveAttacksQueen(self, move):
    #     self.makeMove(move)
    #     #check for a check
    #     if self.whiteToMove:
    #         if self.squareUnderAttack(self.whiteQueenPosition[0], self.whiteQueenPosition[1]):            
    #                 self.undoMove()
    #                 return True
    #     elif not self.whiteToMove:
    #         if self.squareUnderAttack(self.blackQueenPosition[0], self.blackQueenPosition[1]):            
    #                 self.undoMove()
    #                 return True
    #     self.undoMove()
    #     return False



class Move():
    # dictionaries for mapping the propper notation
    rankToRows = {"1": 7, "2": 6, "3": 5,"4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k,v in rankToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,"e": 4, "f": 5,"g": 6,"h": 7}
    colsToFiles = {v: k for k,v in filesToCols.items()}

    def __init__(self, startSq, endSq, board, isEnPassantMove = False, isCastleMove = False, isCheckMove = False, attacksQueen = False, movePriority = 0):
        self.pieceMoved = board[startSq[0]][startSq[1]]
        self.pieceCaptured = board[endSq[0]][endSq[1]]
        self.startSquare = startSq
        self.endSquare = endSq
        self.moveID = self.startSquare[0]*1000 + self.startSquare[1]*100 + self.endSquare[0]*10 + self.endSquare[1]
        # pawn promotion
        self.isPawnPromotion = (self.pieceMoved == 'wP' and self.endSquare[0] == 0) or (self.pieceMoved == 'bP' and self.endSquare[0] == 7)
        # en passant
        self.isEnPassantMove = isEnPassantMove
        if self.isEnPassantMove:
            self.pieceCaptured = "wP" if self.pieceMoved == "bP" else "bP"
        self.isCastleMove = isCastleMove
        self.movePriority = movePriority
        self.isCheckMove = isCheckMove
        self.attacksQueen = attacksQueen


    # overriding the equals function
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startSquare[0], self.startSquare[1]) +  self.getRankFile(self.endSquare[0], self.endSquare[1])

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]

class CastleRights():
    def __init__(self, whiteKingCastle, whiteQueenCastle, blackKingCastle, blackQueenCastle):
        self.whiteKingCastle = whiteKingCastle
        self.whiteQueenCastle = whiteQueenCastle
        self.blackKingCastle = blackKingCastle
        self.blackQueenCastle = blackQueenCastle
