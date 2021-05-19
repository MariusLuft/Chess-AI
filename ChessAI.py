from Engine import GameState
import random
import time
import numpy as np
from operator import attrgetter

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
# number of moves the AI calculates
DEPTH = 4
# evaluation values
CHECKMATE = 1000
STALEMATE = 0
POSITIONWHEIGHT = 0.1
# KINGINCHECK = 0.5
# QUEENUNDERATTACK = 0.2
# MOVINGTWICEPENALTY = -600
EARLYQUEENMOVEPENALTY = -0.7
# ordering values
WINNINGTRADE = 6
EVENTRADE = 3
LOSINGTRADE = 1
PROMOTION = 9
CASTLING = 4
# CHECKMOVE = 5
# ATTACKSQUEEN = 3
# GOODPOSITION = 1


def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]

def findBestMove(gameState, validMoves):
    global nextMove
    global nodesSearched
    nodesSearched = -1
    nextMove = None
    # move ordering
    validMoves = prioritizeMoves(validMoves, gameState) 
    start = time.time()
    findMoveNegaMaxAlphaBeta(gameState, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gameState.whiteToMove else -1)
    end = time.time()
    print("Time spent searching: ", "{:.2f}".format(end - start), " seconds")
    print("Nodes visited: ", nodesSearched)
    return nextMove

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
            nextMoves = prioritizeMoves(nextMoves, gameState) 
            score = -findMoveNegaMaxAlphaBeta(gameState, nextMoves, depth - 1, -beta, -alpha, -turnMultiplyer)          
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
                    print(move.getChessNotation(), score)
            gameState.undoMove()
            if maxScore > alpha:
                alpha = maxScore
            if alpha >= beta:
                break
    return maxScore

def prioritizeMoves(moves,gameState):
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
        # no need to make distinction between check and checkMate here
        # if move.isCheckMove:
        #     move.movePriority  += CHECKMOVE
        # # Queen under attack?
        # if move.attacksQueen:
        #     move.movePriority  += ATTACKSQUEEN
    
    moves.sort(key=lambda move: move.movePriority, reverse=True)
    # moves.sort(key=attrgetter('movePriority'), reverse=True)
    
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
    # # reward checking
    # score += evaluateKingsInCheck(gameState)
    # # rewards attacking the queen
    # score += evaluateQueenUnderAttack(gameState)
    # # punishes slow development
    # score += evaluateSamePieceMovingTwice(gameState)
    # # punishes early queen movement
    score += evaluateEarlyQueenPosition(gameState)
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

# def evaluateKingsInCheck(gameState):
#     score = 0
#     if gameState.blackInCheck:
#         score +=  KINGINCHECK
#     elif gameState.whiteInCheck:
#         score +=  -KINGINCHECK
#     return score

# def evaluateSamePieceMovingTwice(GameState):
#     score = 0
#     # if len(GameState.lastMovedPiecesWhite) > 1:
#     #     if GameState.lastMovedPiecesWhite 
#     if len(GameState.lastMovedPiecesWhite) > 1:
#         if GameState.board[GameState.lastMovedPiecesWhite[-2][0]][GameState.lastMovedPiecesWhite[-2][1]] == "--":
#             score += MOVINGTWICEPENALTY * GameState.lateGameWeight
#     if len(GameState.lastMovedPiecesBlack) > 1:
#         if GameState.board[GameState.lastMovedPiecesBlack[-2][0]][GameState.lastMovedPiecesBlack[-2][1]] == "--":
#             score += -MOVINGTWICEPENALTY * GameState.lateGameWeight

    # if len(GameState.moveLog) > 2:
    #     if (GameState.moveLog[-1].pieceMoved == GameState.moveLog[-3].pieceMoved) and (GameState.moveLog[-1].startSquare == GameState.moveLog[-3].endSquare):
    #         if GameState.moveLog[-1].pieceMoved[0] == 'w':
    #             score += MOVINGTWICEPENALTY * GameState.lateGameWeight
    #         elif GameState.moveLog[-1].pieceMoved[0] == 'b':
    #             score += -MOVINGTWICEPENALTY * GameState.lateGameWeight
    return score

# def evaluateQueenUnderAttack(gameState):
#     score = 0
#     if gameState.blackQueenUnderAttack:
#         score +=  QUEENUNDERATTACK
#     elif gameState.whiteQueenUnderAttack:
#         score +=  -QUEENUNDERATTACK
#     return score

def evaluateEarlyQueenPosition(GameState):
    score = 0
    if GameState.board[7][3] != "wQ":
        score = EARLYQUEENMOVEPENALTY * GameState.lateGameWeight
    if GameState.board[0][3] != "bQ":
        score = -EARLYQUEENMOVEPENALTY * GameState.lateGameWeight
    return score



