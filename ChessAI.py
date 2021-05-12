import random
import time

pieceScore = {"K": 0, "Q": 9, "R":5, "B": 3, "N":3, "P": 1}
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 2

def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]

def findBestMove(gameState, validMoves):
    global nextMove
    global nodesSearched
    nodesSearched = -1
    nextMove = None
    # random.shuffle(validMoves) # variation for testing
    start = time.time()
    findMoveMegaMaxAlphaBeta(gameState, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gameState.whiteToMove else -1)
    end = time.time()
    print("Time spent searching: ", "{:.2f}".format(end - start), " seconds")
    print("Nodes visited: ", nodesSearched)
    return nextMove



# def findMoveMegaMax(gameState, validMoves, depth, turnMultiplyer):
#     global nextMove
#     global nodesSearched 
#     nodesSearched = nodesSearched + 1
#     if depth == 0:
#         return turnMultiplyer * scoreBoard(gameState)
#     maxScore = -CHECKMATE
#     for move in validMoves:
#             gameState.makeMove(move)
#             nextMoves = gameState.getValidMoves()
#             score = -findMoveMegaMax(gameState, nextMoves, depth - 1, -turnMultiplyer)          
#             if score > maxScore:
#                 maxScore = score
#                 if depth == DEPTH:
#                     nextMove = move
#             gameState.undoMove()
#     return maxScore

def findMoveMegaMaxAlphaBeta(gameState, validMoves, depth, alpha, beta, turnMultiplyer):
    global nextMove
    global nodesSearched 
    nodesSearched = nodesSearched + 1

    if depth == 0:
        return turnMultiplyer * scoreBoard(gameState)

    # TODO move ordering        
    
    maxScore = -CHECKMATE
    for move in validMoves:
            gameState.makeMove(move)
            nextMoves = gameState.getValidMoves()
            score = -findMoveMegaMaxAlphaBeta(gameState, nextMoves, depth - 1, -beta, -alpha, -turnMultiplyer)          
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            gameState.undoMove()
            if maxScore > alpha:
                alpha = maxScore
            if alpha >= beta:
                break
    return maxScore




# positive score is good for white
def scoreBoard(gameState):
    # win and draw
    if gameState.checkMate:
        if gameState.whiteToMove:
            return - CHECKMATE
        else:
            return CHECKMATE
    elif gameState.staleMate:
        return STALEMATE
    # material on the board
    score = 0
    for row in gameState.board:
        for square in row:
            if square[0] == 'w': 
                score += pieceScore[square[1]]
            elif square[0] == 'b':
                score -= pieceScore[square[1]]
    # TODO King in check

    # 

    return score 

# def getMaterialScore(board):
#     score = 0
#     for row in board:
#         for square in row:
#             if square[0] == 'w': 
#                 score += pieceScore[square[1]]
#             elif square[0] == 'b':
#                  score -= pieceScore[square[1]]
#     return score 

# def findBestMove(gameState, validMoves):
#     turnMutiplyer = 1 if gameState.whiteToMove else -1
#     opponentsMinMaxScore = CHECKMATE
#     bestPlayerMove = None
#     random.shuffle(validMoves) # adds move variety for testing
#     for playerMove in validMoves:
#         # every legal move for the player
#         gameState.makeMove(playerMove)        
#         opponentsMoves = gameState.getValidMoves()
#         if gameState.checkMate:
#             opponentMaxScore = -CHECKMATE
#         elif gameState.staleMate:
#             opponentMaxScore = STALEMATE
#         else:
#             opponentMaxScore = - CHECKMATE
#         for opponentsMove in opponentsMoves:
#             # finds best response from opponent
#             gameState.makeMove(opponentsMove)
#             gameState.getValidMoves()
#             if gameState.checkMate:
#                 score = CHECKMATE 
#             elif gameState.staleMate:
#                 score = STALEMATE
#             else:
#                 score = -turnMutiplyer * getMaterialScore(gameState.board) # inverted so it's the negative opponent score
#             if score > opponentMaxScore:
#                 opponentMaxScore = score 
#             gameState.undoMove()
#         # if it has the weakest response the move is best for us
#         if opponentMaxScore < opponentsMinMaxScore:
#             opponentsMinMaxScore = opponentMaxScore
#             bestPlayerMove = playerMove
#         gameState.undoMove()
#     return bestPlayerMove

# def findMoveMinMax(gameState, validMoves, depth, whiteToMove):
#     global nextMove
#     global nodesSearched 
#     nodesSearched = nodesSearched + 1
#     if depth == 0:
#         return scoreBoard(gameState)
#     if gameState.whiteToMove:
#         maxScore = -CHECKMATE
#         for move in validMoves:
#             gameState.makeMove(move)
#             nextMoves = gameState.getValidMoves()
#             score = findMoveMinMax(gameState, nextMoves, depth - 1, False)
#             if score > maxScore:
#                 maxScore = score
#                 if depth == DEPTH:
#                     nextMove = move
#             gameState.undoMove()
#         return maxScore
#     else:
#         minScore = CHECKMATE
#         for move in validMoves:
#             gameState.makeMove(move)
#             nextMoves = gameState.getValidMoves()
#             score = findMoveMinMax(gameState, nextMoves, depth - 1, True)
#             if score < minScore:
#                 minScore = score
#                 if depth == DEPTH:
#                     nextMove = move
#             gameState.undoMove()
#         return minScore

    