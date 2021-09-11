# handles user input and displayes the current game state # 

import multiprocessing
import time
import pygame as p
import Engine, ChessAI
from multiprocessing import Process, Queue
import datetime

BOARD_WIDTH = BOARD_HEIGHT = 512
TIME_PANEL_HEIGHT = 100
TIME_PANEL_WIDTH = BOARD_WIDTH
DIMENSION = 8
SQ_SIZE = BOARD_HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

def loadImages():
    pieces = ['wP', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bK', 'bQ', 'bB', 'bN', 'bR', 'bP']

    for piece in pieces:
        IMAGES[piece] = p.image.load("images/" + piece + ".png")
        
def main():
    p.init()
    screen = p.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT + TIME_PANEL_HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    moveSound = p.mixer.Sound('sounds/move.wav')    
    winSound = p.mixer.Sound('sounds/win.wav')   
    gameState = Engine.GameState()
    moveMade = False
    lastMove = None
    validMoves = gameState.getValidMoves()
    gameOverIsSet = False
    #load images only once
    loadImages()
    running = True
    selectedSquare = () # tracks last move
    playerClicks = [] # count mouseclicks
    animate = True
    gameOver = False
    rainbowColors = [(153,0,153), (111,0,255), (0,0,255), (0,204,0), (255,255,0),  (255,128,0),  (255,0,0)]
    endScreenFrameCount = 0
    playerOne = False # True if human, flase if AI, white
    playerTwo = True # black
    timePlayer1 = timePlayer2 = 300
    AIThinking = False
    moveFinderProcess = None
    oldTicks = 0 

    while running: # TODO move event processing to user interaction class
        humanTurn = (gameState.whiteToMove and playerOne) or (not gameState.whiteToMove and playerTwo)
        for e in p.event.get():
            if not gameOver and humanTurn:
                if e.type == p.QUIT:
                    running = False
                # mouse handler
                if e.type == p.MOUSEBUTTONDOWN:
                    location = p.mouse.get_pos() # x,y
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    if selectedSquare == (row, col):
                        selectedSquare = () # undoes the move in progress
                        playerClicks.pop()
                    else: 
                        selectedSquare = (row,col)
                        playerClicks.append(selectedSquare) # counts mouseclick
                    if len(playerClicks) == 2:
                        move = Engine.Move(playerClicks[0],playerClicks[1], gameState.board)
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                print(move.getChessNotation())
                                gameState.makeMove(validMoves[i])
                                moveMade = True
                                animate = True
                                selectedSquare = ()
                                playerClicks = []
                                break
                        if not moveMade:
                            playerClicks = [selectedSquare]
           
            # key handler
            if e.type == p.KEYDOWN:
                if e.key == p.K_n:
                    gameState = Engine.GameState()
                    validMoves = gameState.getValidMoves()
                    selectedSquare = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
                    gameOver = False
                    timePlayer1 = timePlayer2 = 300

        if humanTurn:
            timePlayer2, oldTicks = countTimeForPlayer(timePlayer2, oldTicks, gameOver)   

        # AI choosing a move
        if not gameOver and not humanTurn:            
            if not AIThinking:
                AIThinking = True
                returnQueueBestMove = Queue() # passes data between threads
                moveFinderProcess = Process(target=ChessAI.findBestMove, args=(gameState, validMoves, returnQueueBestMove))
                moveFinderProcess.start() # calls find best move asynchronally


            if not moveFinderProcess.is_alive():
                AIMove = returnQueueBestMove.get()
                if AIMove is None:
                    AIMove = ChessAI.findRandomMove(validMoves)
                gameState.makeMove(AIMove)
                print(AIMove.getChessNotation())
                moveMade = True
                animate = True
                AIThinking = False
            timePlayer1, oldTicks = countTimeForPlayer(timePlayer1, oldTicks, gameOver)

        if moveMade:
            moveSound.play()
            if animate:
                animateMove(gameState.moveLog[-1], screen, gameState.board, clock)            
            if gameState.earlyGameWeight >= 0.05:
                gameState.earlyGameWeight -= 0.05
            validMoves = gameState.getValidMoves()
            moveMade = False
            animate = False     
            lastMove = gameState.moveLog[-1]

        drawGameState(screen, gameState, validMoves, selectedSquare, lastMove, timePlayer1, timePlayer2, gameOver)

        # checks if game is over
        if gameState.checkMate or gameState.staleMate or timePlayer1 <= 0 or timePlayer2 <= 0: 
            if not gameOverIsSet:
                gameOver = True            
                winSound.play()
            endScreenFrameCount = endScreenFrameCount + 1
            displayGameOverText(screen, gameState, endScreenFrameCount,rainbowColors, timePlayer1, timePlayer2) 
            gameOverIsSet = True
        

        clock.tick(MAX_FPS)
        p.display.flip()


def displayGameOverText(screen, gameState, endScreenFrameCount,rainbowColors, timePlayer1, timePlayer2): 
    index = (endScreenFrameCount % 70) // 10 - 1
    color = p.Color(rainbowColors[index][0],rainbowColors[index][1],rainbowColors[index][2])
    if gameState.checkMate:
        gameOver = True
        if gameState.whiteToMove:
            drawEndGameText(screen, "Black won!",color)
        if not gameState.whiteToMove:
            drawEndGameText(screen, "White won!",color)
    elif gameState.staleMate:
        gameOver = True
        drawEndGameText(screen, "Draw!",color)
    elif timePlayer1 <= 0:
        gameOver = True
        drawEndGameText(screen, "Black won on time!",color)
    elif timePlayer2 <= 0:
        gameOver = True
        drawEndGameText(screen, "White won on time!",color)
       

def highlightSquares(screen, gameState, validMoves, selectedSquare):
    if selectedSquare != ():
        r,c = selectedSquare
        if gameState.board[r][c][0] == ('w' if gameState.whiteToMove else 'b'): # is it no empty square?
            # highlights selected square
            s = p.Surface((SQ_SIZE,SQ_SIZE))
            s.set_alpha(100)
            s.fill(p.Color('blue'))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            # highlights valid moves
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startSquare[0] == r and move.startSquare[1] == c:
                    screen.blit(s, (move.endSquare[1] * SQ_SIZE, move.endSquare[0] * SQ_SIZE))

def highlightLastMove(screen, gameState, lastMove):
    if len(gameState.moveLog) > 0:
        s = p.Surface((SQ_SIZE,SQ_SIZE))
        s.set_alpha(100)
        s.fill(p.Color('orange'))
        screen.blit(s, (lastMove.endSquare[1] * SQ_SIZE, lastMove.endSquare[0] * SQ_SIZE))


def drawGameState(screen, gameState, validMoves, selectedSquare, lastMove, timePlayer1, timePlayer2, gameOver): 
    drawBoard(screen)
    highlightSquares(screen, gameState, validMoves, selectedSquare)
    highlightLastMove(screen, gameState, lastMove)
    drawPieces(screen, gameState.board)
    drawTimeBoard(screen, timePlayer1, timePlayer2, gameOver)


def drawBoard(screen):
    global colors
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c)%2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE,SQ_SIZE))

def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE,SQ_SIZE))

def animateMove(move, screen, board, clock):
    global colors
    deltaRow = move.endSquare[0] - move.startSquare[0]
    deltaCol = move.endSquare[1] - move.startSquare[1]
    framesPerSquare = 3
    frameCount = (abs(deltaCol) + abs(deltaRow)) * framesPerSquare
    for frame in range(frameCount + 1):
        r,c = (move.startSquare[0] + deltaRow  *  frame / frameCount, move.startSquare[1] + deltaCol  *  frame / frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        # erase moving piece from its ending square
        color = colors[(move.endSquare[0] + move.endSquare[1]) % 2]
        endSquare = p.Rect(move.endSquare[1] * SQ_SIZE, move.endSquare[0] * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        # draw captured piece onto rectangle 
        if move.pieceCaptured != "--":
            if move.isEnPassantMove:
                enPassantRow = move.endSquare[0] + 1 if move.pieceCaptured[0] == 'b' else move.endSquare[0] - 1
                endSquare = p.Rect(move.endSquare[1] * SQ_SIZE, enPassantRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        # draw moving pieces 
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)

def drawEndGameText(screen, text, fontColor):
    font = p.font.SysFont("comicsansms", 64)
    textObject = font.render(text, 0, fontColor)
    textLocation = p.Rect(0,0, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH/2 - textObject.get_width()/2, BOARD_HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)

def drawTimeBoard(screen, timePlayer1, timePlayer2, gameOver): 
    timeRect = p.Rect(0, BOARD_HEIGHT, TIME_PANEL_WIDTH, TIME_PANEL_HEIGHT)
    p.draw.rect(screen, p.Color("black"), timeRect)
    font = p.font.SysFont("comicsansms", 24)
    stringTimePlayer2 = str(datetime.timedelta(seconds=timePlayer2))
    stringTimePlayer1 = str(datetime.timedelta(seconds=timePlayer1))
    text = "Human:   " + stringTimePlayer2 + "   AI:   " + stringTimePlayer1
    textObject = font.render(text, 0, p.Color('gray'))
    textLocation = p.Rect(50, BOARD_HEIGHT + 30, TIME_PANEL_WIDTH, TIME_PANEL_HEIGHT)
    screen.blit(textObject, textLocation)

def countTimeForPlayer(timePlayer, oldTicks, gameOver):
    # frame count since game started
    current_ticks= p.time.get_ticks()        
    if current_ticks - oldTicks >= 1000 and timePlayer > 0 and not gameOver:
        timePlayer -= 1
        oldTicks = current_ticks
    return timePlayer, oldTicks









if __name__ == "__main__":
    # Pyinstaller fix
    multiprocessing.freeze_support()
    main()

