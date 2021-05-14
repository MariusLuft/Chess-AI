import random
import time
import numpy as np

pieceScore = {"K": 0, "Q": 9, "R":5, "B": 3, "N":3, "P": 1}
knightScores = [(1, 2, 3, 3, 3, 3, 2, 1),
                (2, 4, 5, 5, 5, 5, 4, 2),
                (3, 5, 6, 6, 6, 6, 5, 3),
                (3, 5, 6, 7, 7, 6, 5, 3),
                (3, 5, 6, 7, 7, 6, 5, 3),
                (3, 5, 6, 6, 6, 6, 5, 3),
                (2, 4, 5, 5, 5, 5, 4, 2),
                (1, 2, 3, 3, 3, 3, 2, 1),]
kingScoresWhite = [(2, 2, 2, 1, 1, 2, 2, 2),
                   (2, 2, 2, 1, 1, 2, 2, 2),
                   (2, 2, 2, 1, 1, 2, 2, 2),
                   (2, 2, 2, 1, 1, 2, 2, 2),
                   (3, 2, 2, 1, 1, 2, 2, 3),
                   (3, 4, 4, 4, 4, 4, 4, 3),
                   (5, 5, 4, 4, 4, 4, 5, 5),
                   (5, 7, 6, 4, 4, 5, 7, 5)]
kingScoresBlack = [(5, 7, 6, 4, 4, 5, 7, 5),
                   (5, 5, 4, 4, 4, 4, 5, 5),
                   (3, 4, 4, 4, 4, 4, 4, 3),
                   (3, 2, 2, 1, 1, 2, 2, 3),
                   (2, 2, 2, 1, 1, 2, 2, 2),
                   (2, 2, 2, 1, 1, 2, 2, 2),
                   (2, 2, 2, 1, 1, 2, 2, 2),
                   (2, 2, 2, 1, 1, 2, 2, 2)]
queenScores =     [(1, 2, 2, 3, 3, 2, 2, 1),
                   (2, 4, 5, 6, 6, 5, 4, 2),
                   (2, 5, 7, 7, 7, 7, 5, 2),
                   (4, 5, 7, 7, 7, 7, 5, 4),
                   (4, 5, 7, 7, 7, 7, 5, 4),
                   (2, 5, 7, 7, 7, 7, 5, 2),
                   (2, 4, 5, 6, 6, 5, 4, 2),
                   (1, 2, 2, 3, 3, 2, 2, 1)]
rookScoresWhite = [(5, 5, 5, 5, 5, 5, 5, 5),
                   (6, 7, 7, 7, 7, 7, 7, 6),
                   (1, 3, 3, 3, 3, 3, 3, 1),
                   (1, 3, 3, 3, 3, 3, 3, 1),
                   (1, 3, 3, 3, 3, 3, 3, 1),
                   (1, 3, 3, 3, 3, 3, 3, 1),
                   (1, 3, 3, 3, 3, 3, 3, 1),
                   (3, 3, 3, 6, 6, 4, 3, 3)]
rookScoresBlack = [(3, 3, 3, 6, 6, 4, 3, 3),
                   (1, 3, 3, 3, 3, 3, 3, 1),
                   (1, 3, 3, 3, 3, 3, 3, 1),
                   (1, 3, 3, 3, 3, 3, 3, 1),
                   (1, 3, 3, 3, 3, 3, 3, 1),
                   (1, 3, 3, 3, 3, 3, 3, 1),
                   (6, 7, 7, 7, 7, 7, 7, 6),
                   (5, 5, 5, 5, 5, 5, 5, 5)]
bishopScoresWhite = [(1, 3, 4, 6, 6, 4, 3, 1),
                   (2, 4, 4, 4, 4, 4, 4, 2),
                   (2, 5, 4, 6, 6, 4, 5, 2),
                   (2, 5, 5, 6, 6, 5, 5, 2),
                   (2, 5, 7, 6, 6, 7, 5, 2),
                   (2, 5, 6, 6, 6, 6, 5, 2),
                   (2, 5, 5, 5, 5, 5, 5, 2),
                   (5, 2, 2, 2, 2, 2, 2, 5)]
bishopScoresBlack = [(5, 2, 2, 2, 2, 2, 2, 5),
                   (2, 5, 5, 5, 5, 5, 5, 2),
                   (2, 5 , 6, 6, 6, 6, 5, 2),
                   (2, 5, 7, 6, 6, 7, 5, 2),
                   (2, 5, 5, 6, 6, 5, 5, 2),
                   (2, 5, 4, 6, 6, 4, 5, 2),
                   (2, 4, 4, 4, 4, 4, 4, 2),
                   (1, 3, 4, 6, 6, 4, 3, 1)]
pawnScoresWhite = [(3, 3, 3, 3, 3, 3, 3, 3),
                   (7, 7, 7, 7, 7, 7, 7, 7),
                   (3, 3, 3, 6, 6, 3, 3, 3),
                   (3, 3, 3, 6, 6, 3, 3, 3),
                   (3, 3, 3, 6, 6, 3, 3, 3),
                   (2, 3, 2, 4, 4, 2, 3, 2),
                   (4, 5, 5, 1, 1, 5, 5, 4),
                   (3, 3, 3, 3, 3, 3, 3, 3)]
pawnScoresBlack = [(3, 3, 3, 3, 3, 3, 3, 3),
                   (4, 5, 5, 1, 1, 5, 5, 4),
                   (2, 3, 2, 4, 4, 2, 3, 2),
                   (3, 3, 3, 6, 6, 3, 3, 3),
                   (3, 3, 3, 6, 6, 3, 3, 3),
                   (3, 3, 3, 6, 6, 3, 3, 3),
                   (7, 7, 7, 7, 7, 7, 7, 7),
                   (3, 3, 3, 3, 3, 3, 3, 3)]
piecePositionScoresWhite = {"K": kingScoresWhite, "Q": queenScores, "R":rookScoresWhite, "B": bishopScoresWhite, "N": knightScores, "P": pawnScoresWhite}
piecePositionScoresBlack = {"K": kingScoresBlack, "Q": queenScores, "R":rookScoresBlack, "B": bishopScoresBlack, "N": knightScores, "P": pawnScoresBlack}
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 3
POSITIONWHEIGHT = 0.11
WINNINGTRADE = 6
EVENTRADE = 3
LOSINGTRADE = 1
PROMOTION = 9
CASTLING = 4


def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]

def findBestMove(gameState, validMoves):
    global nextMove
    global nodesSearched
    nodesSearched = -1
    nextMove = None
    # move ordering
    validMoves = prioritizeMoves(validMoves) 
    start = time.time()
    findMoveNegaMaxAlphaBeta(gameState, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gameState.whiteToMove else -1)
    # findMoveMegaMax(gameState, validMoves, DEPTH, 1 if gameState.whiteToMove else -1)
    # findMoveMinMax(gameState, validMoves, DEPTH, gameState.whiteToMove)
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

def findMoveNegaMaxAlphaBeta(gameState, validMoves, depth, alpha, beta, turnMultiplyer):
    global nextMove
    global nodesSearched 
    nodesSearched = nodesSearched + 1

    if depth == 0:
        return turnMultiplyer * scoreBoard(gameState)
    
    maxScore = -CHECKMATE
    for move in validMoves:
            gameState.makeMove(move)
            nextMoves = gameState.getValidMoves()
            # move ordering
            nextMoves = prioritizeMoves(nextMoves) 
            score = -findMoveNegaMaxAlphaBeta(gameState, nextMoves, depth - 1, -beta, -alpha, -turnMultiplyer)          
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

def prioritizeMoves(moves):
    for move in moves:
        move.movePriority = 0 # reset
        # trade value
        if move.pieceCaptured != "--":
            tradeValue = (pieceScore[move.pieceCaptured[1]] - pieceScore[move.pieceMoved[1]])
            # winning trade
            if tradeValue > 0:
                move.movePriority  += WINNINGTRADE
            elif tradeValue == 0:
            # even trade
                move.movePriority  += EVENTRADE
            # loosing trade
            else:
                move.movePriority  += LOSINGTRADE            
        # promotions
        if move.isPawnPromotion:
            move.movePriority  += PROMOTION
        # castling
        elif move.isCastleMove:
            move.movePriority  += CASTLING
        # check
        # checkmate
        # Queen under attack?
        # does the position improve?
        
    
    moves.sort(key=lambda move: move.movePriority, reverse=True)
    
    return moves






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
    
    score = 0
    for row in range(len(gameState.board)):
        for col in range(len(gameState.board[row])):
            square = gameState.board[row][col]
            if square != "--":
                # piece position and material value
                score = evaluateMaterialConsideringPosition(square, score, row, col)
                # evaluate King Safety
                # punish double pawns
                # punish hanging pieces
                # reward protected pieces
                # reward attacked pieces
                # preserved castle rights
    return score 

def evaluateMaterialConsideringPosition(square, score, row, col):
    piecePositionScore = 0
    if square[0] == 'w': 
        piecePositionScore += piecePositionScoresWhite[square[1]][row][col]
        score += pieceScore[square[1]] + piecePositionScore * POSITIONWHEIGHT                
    else:
        piecePositionScore += piecePositionScoresBlack[square[1]][row][col]
        score -= pieceScore[square[1]] + piecePositionScore * POSITIONWHEIGHT
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
#                 score = -turnMutiplyer * scoreBoard(gameState) # inverted so it's the negative opponent score
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

    