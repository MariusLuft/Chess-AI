import random

pieceScore = {"K": 0, "Q": 9, "R":5, "B": 3, "N":3, "P": 1}
CHECKMATE = 1000
STALEMATE = 0

def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]

def findBestMove(gameState, validMoves):
    turnMutiplyer = 1 if gameState.whiteToMove else -1
    opponentsMinMaxScore = CHECKMATE
    bestPlayerMove = None
    for playerMove in validMoves:
        # every legal move for the player
        gameState.makeMove(playerMove)        
        opponentsMoves = gameState.getValidMoves()
        opponentMaxScore = - CHECKMATE
        for opponentsMove in opponentsMoves:
            # finds best response from opponent
            gameState.makeMove(opponentsMove)
            if gameState.checkMate:
                score = -turnMutiplyer *  CHECKMATE # inverted so it's the negative opponent score
            elif gameState.staleMate:
                score = STALEMATE
            else:
                score = -turnMutiplyer * getMaterialScore(gameState.board) # inverted so it's the negative opponent score
            if score > opponentMaxScore:
                opponentMaxScore = score 
            gameState.undoMove()
        # if it has the weakest response the move is best for us
        if opponentMaxScore < opponentsMinMaxScore:
            opponentsMinMaxScore = opponentMaxScore
            bestPlayerMove = playerMove
        gameState.undoMove()
    return bestPlayerMove

def getMaterialScore(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w': 
                score += pieceScore[square[1]]
            elif square[0] == 'b':
                 score -= pieceScore[square[1]]
    return score 

    