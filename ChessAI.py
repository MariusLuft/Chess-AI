from Engine import GameState
import random
import time
import numpy as np
from operator import attrgetter
import math

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

def findBestMove(gameState, validMoves, returnQueue):
    global nextMove
    global nodesSearched
    nodesSearched = -1
    nextMove = None
    start = time.time()
    findMoveNegaMaxAlphaBeta(gameState, DEPTH, -math.inf, math.inf, 1 if gameState.whiteToMove else -1)
    end = time.time()
    print("Time spent searching: ", "{:.2f}".format(end - start), " seconds")
    print("Nodes visited: ", nodesSearched)
    returnQueue.put(nextMove)

def findMoveNegaMaxAlphaBeta(gameState, depth, alpha, beta, turnMultiplyer):

    # value: stores highest score of child generation
    global nextMove
    global nodesSearched 
    nodesSearched = nodesSearched + 1
    
    # get children moves
    childNodes = gameState.getValidMoves()

    # reaches end and return score
    if depth == 0 or len(childNodes) == 0:
        if gameState.whiteToMove:
            return turnMultiplyer * scoreBoard(gameState) + depth
        else:
            return turnMultiplyer * scoreBoard(gameState) - depth
        

    # move ordering
    childNodes = prioritizeMoves(childNodes) 

    # first set to minimum
    maxValue = -math.inf
    
    # loops through possible moves
    for child in childNodes: 

            # make the move
            gameState.makeMove(child)
            
            # next generation
            value = -findMoveNegaMaxAlphaBeta(gameState, depth - 1, -beta, -alpha, -turnMultiplyer)                      

            if maxValue < value:
                maxValue = value
                # original move
                if depth == DEPTH:                   
                    # best of the original moves                
                    nextMove = child
                    

            # unmake move 
            gameState.undoMove()

            # increase alpha
            alpha = max(alpha, maxValue)

            # cut off
            if alpha >= beta:
                break                       

    return maxValue

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
    
    moves.sort(key=lambda move: move.movePriority, reverse=True)
    
    return moves


# positive score is good for white
def scoreBoard(gameState):
    # win and draw
    if gameState.checkMate:
        if gameState.whiteToMove:
            return -CHECKMATE
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

def evaluateLateKingPosition(gameState, scoreSoFar):
    score = 0

    # kings distance to the center
    backKingRow = gameState.blackKingPosition[0]
    blackKingCol = gameState.blackKingPosition[1]
    whiteKingRow = gameState.whiteKingPosition[0]
    whiteKingCol = gameState.whiteKingPosition[1]

    blackKingDstToCenterRow = max(3 - backKingRow, backKingRow - 4)
    blackKingDstToCenterCol = max(3 - blackKingCol, blackKingCol - 4)
    blackKingDstToCenter = blackKingDstToCenterRow + blackKingDstToCenterCol

    whiteKingDstToCenterRow = max(3 - whiteKingRow, whiteKingRow - 4)
    whiteKingDstToCenterCol = max(3 - whiteKingCol, whiteKingCol - 4)
    whiteKingDstToCenter = whiteKingDstToCenterRow + whiteKingDstToCenterCol

    score = blackKingDstToCenter - whiteKingDstToCenter 

    # kings distance from each other
    if scoreSoFar > 0: # white is winning
        distanceBetweenKingsRow = abs(backKingRow - whiteKingRow)
        distanceBetweenKingsCol = abs(blackKingCol - whiteKingCol)
        distanceBetweenKings = distanceBetweenKingsRow + distanceBetweenKingsCol
        score += 15 - distanceBetweenKings
    elif scoreSoFar < 0: # black is winning
        distanceBetweenKingsRow = abs(backKingRow - whiteKingRow)
        distanceBetweenKingsCol = abs(blackKingCol - whiteKingCol)
        distanceBetweenKings = distanceBetweenKingsRow + distanceBetweenKingsCol
        score += distanceBetweenKings - 15

    return score * gameState.lateGameWeight


def evaluateEarlyQueenPosition(GameState):
    score = 0
    if GameState.board[7][3] != "wQ":
        score = EARLYQUEENMOVEPENALTY * GameState.earlyGameWeight
    if GameState.board[0][3] != "bQ":
        score = -EARLYQUEENMOVEPENALTY * GameState.earlyGameWeight
    return score



