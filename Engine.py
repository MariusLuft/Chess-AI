# storing information about the state of the chess game and determening the valid moves # 
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
        self.whiteToMove = True
        self.moveLog = []
        self.moveFunctions = {'P': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getNightMoves, 'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}
        self.whiteKingPosition = (7,4)
        self.blackKingPosition = (0,4)
        self.checkMate = False
        self.staleMate = False
        self.possibleEnPassantSquare = ()
        self.currentCastlingRights = CastleRights(True, True, True, True)
        self.castleRightsLog = [ CastleRights(self.currentCastlingRights.whiteKingCastle, self.currentCastlingRights.whiteQueenCastle, self.currentCastlingRights.blackKingCastle, self.currentCastlingRights.blackQueenCastle)]

    # moves pieces on board except casteling, en-passant and pawn capture
    def makeMove(self, move):
        self.board[move.startSquare[0]][move.startSquare[1]] = "--"
        self.board[move.endSquare[0]][move.endSquare[1]] = move.pieceMoved
        self.moveLog.append(move) # log to be able to undo moves
        self.whiteToMove = not self.whiteToMove # players take turns        
        if move.pieceMoved == "wK" or move.pieceMoved == "bK":
            self.updateKingPosition(move)
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
        # castling
        if move.isCastleMove:
            if  move.endSquare[1] - move.startSquare[1] == 2: # Kingside castling
                self.board[move.startSquare[0]][move.endSquare[1] - 1] = self.board[move.startSquare[0]][move.endSquare[1] + 1] # copies the rook
                self.board[move.startSquare[0]][move.endSquare[1] + 1] = "--" # removes the rook
            else: # queen side catling
                self.board[move.startSquare[0]][move.endSquare[1] + 1] = self.board[move.startSquare[0]][move.endSquare[1] - 2] # copies the rook
                self.board[move.startSquare[0]][move.endSquare[1] - 2] = "--" # removes the rook

        self.updateCastleRights(move)
        self.castleRightsLog.append(CastleRights(self.currentCastlingRights.whiteKingCastle, self.currentCastlingRights.whiteQueenCastle, self.currentCastlingRights.blackKingCastle, self.currentCastlingRights.blackQueenCastle))
        lastMove = move
        

             

    def undoMove(self):
        if len(self.moveLog)>0:
            move = self.moveLog.pop()
            self.board[move.startSquare[0]][move.startSquare[1]] = move.pieceMoved
            self.board[move.endSquare[0]][move.endSquare[1]] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            if move.pieceMoved == "wK" or move.pieceMoved == "bK":
                self.reverseKingPosition(move)
            # undo en passant
            if move.isEnPassantMove:
                self.board[move.endSquare[0]][move.endSquare[1]] = "--" # leave landing square blank
                self.board[move.startSquare[0]][move.endSquare[1]] = move.pieceCaptured
                self.possibleEnPassantSquare = (move.endSquare[0], move.endSquare[1])
            # undo 2 square pawn move
            elif move.pieceMoved[1] == 'P' and abs(move.startSquare[0] - move.endSquare[0]) == 2:
                self.possibleEnPassantSquare = ()
            # undo castling rights
            self.castleRightsLog.pop()
            self.currentCastlingRights = CastleRights(self.castleRightsLog[-1].whiteKingCastle, self.castleRightsLog[-1].whiteQueenCastle, self.castleRightsLog[-1].blackKingCastle, self.castleRightsLog[-1].blackQueenCastle)
            # undo castling move
            if move.isCastleMove:
                if  move.endSquare[1] - move.startSquare[1] == 2: # Kingside castling
                    self.board[move.startSquare[0]][move.endSquare[1] + 1] = self.board[move.startSquare[0]][move.endSquare[1] - 1] # copies the rook
                    self.board[move.startSquare[0]][move.endSquare[1] - 1] = "--" # removes the rook
                else: # queen side catling
                    self.board[move.startSquare[0]][move.endSquare[1] - 2] = self.board[move.startSquare[0]][move.endSquare[1] + 1] # copies the rook
                    self.board[move.startSquare[0]][move.endSquare[1] + 1] = "--" # removes the rook

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
        tempEnPassantSquare = self.possibleEnPassantSquare
        tempCastleRights = CastleRights(self.currentCastlingRights.whiteKingCastle, self.currentCastlingRights.whiteQueenCastle, self.currentCastlingRights.blackKingCastle, self.currentCastlingRights.blackQueenCastle)
        moves = self.getPossibleMoves()
        if self.whiteToMove:
            self.getCastleMoves(self.whiteKingPosition[0], self.whiteKingPosition[1], moves)
        else:
            self.getCastleMoves(self.blackKingPosition[0], self.blackKingPosition[1], moves)
        for i in range(len(moves) -1, -1, -1): # search list backwards to avoid bugs after deleting elements
            self.makeMove(moves[i])
            self.whiteToMove = not self.whiteToMove 
            if self.isInCheck():
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove 
            self.undoMove()
        if len(moves) == 0:
            if self.isInCheck:
                self.checkMate = True
            else:
                self.staleMate = True
        else:   # reverses checkmate in case of undo
            self.checkMate = False
            self.staleMate = False

        self.possibleEnPassantSquare = tempEnPassantSquare
        self.currentCastlingRights = tempCastleRights
        return moves

    # determines if the current player is in check
    def isInCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingPosition[0], self.whiteKingPosition[1])
        else:
            return self.squareUnderAttack(self.blackKingPosition[0], self.blackKingPosition[1])

    # determines if a certain fiel is under attack
    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove # switches turn
        opponentsMoves = self.getPossibleMoves()
        self.whiteToMove = not self.whiteToMove # reverses turn back to normal
        for move in opponentsMoves:
            if move.endSquare[0] == r and move.endSquare[1] == c:
                return True
        return False 

    def updateKingPosition(self, move):
        if move.pieceMoved == "wK":
            self.whiteKingPosition = (move.endSquare[0], move.endSquare[1])
        elif move.pieceMoved == "bK":
            self.blackKingPosition = (move.endSquare[0], move.endSquare[1])

    def reverseKingPosition(self, move):
        if move.pieceMoved == "wK":
            self.whiteKingPosition = (move.startSquare[0], move.startSquare[1])
        if move.pieceMoved == "bK":
            self.blackKingPosition = (move.startSquare[0], move.startSquare[1])

    # update castle rights if king or rook move
    def updateCastleRights(self, move):
        if move.pieceMoved == "wK":
            self.currentCastlingRights.whiteKingCastle = False
            self.currentCastlingRights.whiteQueenCastle = False
        elif move.pieceMoved == "bK":
            self.currentCastlingRights.blackKingCastle = False
            self.currentCastlingRights.blackQueenCastle = False
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
        # TODO what if the rook gets captured?

            
    # generates possible moves for Pawns
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove: # whites turn
            if self.board[r-1][c] == "--": # pawn moves 1 field
                moves.append(Move((r,c), (r-1,c), self.board))
                if r == 6 and self.board[r-2][c] == "--": # pawn moves 2 fields
                    moves.append(Move((r,c), (r-2,c), self.board))
            if c+1 <= 7:
                if self.board[r-1][c + 1][0] == 'b': # enemy piece
                    moves.append(Move((r,c), (r-1,c +1), self.board))
                elif (r-1,c +1) == self.possibleEnPassantSquare: # en passant
                    moves.append(Move((r,c), (r-1,c +1), self.board, isEnPassantMove = True))
            if c-1 >= 0:
                if self.board[r-1][c - 1][0] == 'b': # enemy piece
                    moves.append(Move((r,c), (r-1,c -1), self.board))
                elif (r-1,c -1) == self.possibleEnPassantSquare: # en passant
                    moves.append(Move((r,c), (r-1,c -1), self.board, isEnPassantMove = True))
        else: # blacks turn
            if self.board[r+1][c] == "--": # pawn moves 1 field
                moves.append(Move((r,c), (r+1,c), self.board))
                if r == 1 and self.board[r+2][c] == "--": # pawn moves 2 fields
                    moves.append(Move((r,c), (r+2,c), self.board))
            if c+1 <= 7:
                if self.board[r+1][c + 1][0] == 'w': # enemy piece
                    moves.append(Move((r,c), (r+1,c +1), self.board))
                elif (r+1,c +1) == self.possibleEnPassantSquare: # en passant
                    moves.append(Move((r,c), (r+1,c +1), self.board, isEnPassantMove = True))
            if c-1 >= 0:
                if self.board[r+1][c - 1][0] == 'w': # enemy piece
                    moves.append(Move((r,c), (r+1,c -1), self.board))
                elif (r+1,c -1) == self.possibleEnPassantSquare: # en passant
                    moves.append(Move((r,c), (r+1,c -1), self.board, isEnPassantMove = True))

    # generates possible moves for Rooks
    def getRookMoves(self, r, c, moves):
        enemyColor = 'b' if self.whiteToMove else 'w'
        # move upwards
        for fields in range(1, r + 1):
            if self.board[r-fields][c] == "--":
                moves.append(Move((r,c), (r-fields,c), self.board))
            else:
                if self.board[r-fields][c][0] == enemyColor:
                    moves.append(Move((r,c), (r-fields,c), self.board))
                    break
                break
        # move right
        for fields in range(1, 8 - c):
            if self.board[r][c+fields] == "--":
                moves.append(Move((r,c), (r,c+fields), self.board))
            else:
                if self.board[r][c+fields][0] == enemyColor:
                    moves.append(Move((r,c), (r,c+fields), self.board))
                    break
                break
        # move left
        for fields in range(1, c + 1):
            if self.board[r][c-fields] == "--":
                moves.append(Move((r,c), (r,c-fields), self.board))
            else:
                if self.board[r][c-fields][0] == enemyColor:
                    moves.append(Move((r,c), (r,c-fields), self.board))
                    break
                break
            # move down
        for fields in range(1, 8 - r):
            if self.board[r + fields][c] == "--":
                moves.append(Move((r,c), (r+fields,c), self.board))
            else:
                if self.board[r + fields][c][0] == enemyColor:
                    moves.append(Move((r,c), (r+fields,c), self.board))
                    break
                break

    # generates possible moves for Nights
    def getNightMoves(self, r, c, moves):
        allyColor = 'w' if self.whiteToMove else 'b'
        knightMoves = ((-2,1),(2,-1), (2,1),(-2,-1), (1,2), (-1,2), (-1,-2), (1,-2)) 
        for move in knightMoves:
            endrow = r + move[0]
            endcol = c + move[1]
            if 0 <= endrow < 8 and 0 <= endcol < 8:
                endpiece = self.board[endrow][endcol]
                if endpiece[0] != allyColor:
                    moves.append(Move((r,c), (endrow,endcol), self.board))

    # generates possible moves for Bishops
    def getBishopMoves(self, r, c, moves):
        enemyColor = 'b' if self.whiteToMove else 'w'
        # move diagonally up right
        for fields in range(1, min(r + 1, 8 - c)):
            if self.board[r-fields][c + fields] == "--":
                moves.append(Move((r,c), (r-fields,c+ fields), self.board))
            else:
                if self.board[r-fields][c + fields][0] == enemyColor:
                    moves.append(Move((r,c), (r-fields,c+ fields), self.board))
                    break
                break
        # move diagonally up left
        for fields in range(1, min(r + 1, c + 1)):
            if self.board[r-fields][c - fields] == "--":
                moves.append(Move((r,c), (r-fields,c- fields), self.board))
            else:
                if self.board[r-fields][c - fields][0] == enemyColor:
                    moves.append(Move((r,c), (r-fields,c- fields), self.board))
                    break
                break
        # move diagonally down right
        for fields in range(1, min(8 - r, 8 - c)):
            if self.board[r+fields][c + fields] == "--":
                moves.append(Move((r,c), (r+fields,c+ fields), self.board))
            else:
                if self.board[r+fields][c + fields][0] == enemyColor:
                    moves.append(Move((r,c), (r+fields,c+ fields), self.board))
                    break
                break
        # move diagonally down left
        for fields in range(1, min(8 - r, c + 1)):
            if self.board[r+fields][c - fields] == "--":
                moves.append(Move((r,c), (r+fields,c- fields), self.board))
            else:
                if self.board[r+fields][c - fields][0] == enemyColor:
                    moves.append(Move((r,c), (r+fields,c- fields), self.board))
                    break
                break
        
    # generates possible moves for Queens
    def getQueenMoves(self, r, c, moves):
        self.getBishopMoves(r, c, moves)
        self.getRookMoves(r, c, moves)

    # generates possible moves for Kings
    def getKingMoves(self, r, c, moves):
        enemyColor = 'b' if self.whiteToMove else 'w'
        # move upwards            
        if r-1>=0:
            if self.board[r-1][c] == "--" or self.board[r-1][c][0] == enemyColor:
                moves.append(Move((r,c), (r-1,c), self.board))    
        # move down            
        if r+1<=7:
            if self.board[r+1][c] == "--" or self.board[r+1][c][0] == enemyColor:
                moves.append(Move((r,c), (r+1,c), self.board))    
        # move left            
        if c-1>=0:
            if self.board[r][c-1] == "--" or self.board[r][c-1][0] == enemyColor:
                moves.append(Move((r,c), (r,c-1), self.board))
            # move right            
        if c+1<=7:
            if self.board[r][c+1] == "--" or self.board[r][c+1][0] == enemyColor:
                moves.append(Move((r,c), (r,c+1), self.board))
        # move diagonally up right
        if r-1>=0 and c+1<=7:
            if self.board[r-1][c +1] == "--" or self.board[r-1][c +1][0] == enemyColor:
                moves.append(Move((r,c), (r-1,c+1), self.board))
                # move diagonally up left
        if r-1>=0 and c-1>=0:
            if self.board[r-1][c -1] == "--" or self.board[r-1][c -1][0] == enemyColor:
                moves.append(Move((r,c), (r-1,c-1), self.board))
                # move diagonally down right
        if r+1<=7 and c+1<=7:
            if self.board[r+1][c +1] == "--" or self.board[r+1][c +1][0] == enemyColor:
                moves.append(Move((r,c), (r+1,c+1), self.board))
                # move diagonally down left
        if r+1<=7 and c-1>=0:
            if self.board[r+1][c -1] == "--" or self.board[r+1][c -1][0] == enemyColor:
                moves.append(Move((r,c), (r+1,c-1), self.board))

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
            if not self.squareUnderAttack(r,c-11) and not self.squareUnderAttack(r,c-22):
                moves.append(Move((r,c), (r,c-2), self.board, isCastleMove = True))


class Move():
    # dictionaries for mapping the propper notation
    rankToRows = {"1": 7, "2": 6, "3": 5,"4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k,v in rankToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,"e": 4, "f": 5,"g": 6,"h": 7}
    colsToFiles = {v: k for k,v in filesToCols.items()}

    def __init__(self, startSq, endSq, board, isEnPassantMove = False, isCastleMove = False):
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
