import random

pieceScore = {"K": 0, "Q": 9, "R":5, "B": 3, "N":3, "P": 1}
CHECKMATE = 1000
STALEMATE = 0

def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]

def findBestMove(gameState, validMoves):
    turnMutiplyer = 1 if gameState.whiteToMove else -1
    maxScore = -CHECKMATE
    bestMove = None
    for playerMove in validMoves:
        gameState.makeMove(playerMove)        
        if gameState.checkMate:
            score = CHECKMATE
        elif gameState.staleMate:
            score = STALEMATE
        else:
            score = turnMutiplyer * getMaterialScore(gameState.board) # makes the score positive for easy comparison
        if score > maxScore:
            maxScore = score
            bestMove = playerMove
        gameState.undoMove()
    return bestMove

def getMaterialScore(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w': 
                score += pieceScore[square[1]]
            elif square[0] == 'b':
                 score -= pieceScore[square[1]]
    return score 

    