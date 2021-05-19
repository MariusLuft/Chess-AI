# handles user input and displayes the current game state # 

import pygame as p
import Engine, ChessAI
import numpy 

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

def loadImages():
    pieces = ['wP', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bK', 'bQ', 'bB', 'bN', 'bR', 'bP']

    for piece in pieces:
        IMAGES[piece] = p.image.load("images/" + piece + ".png")
        
def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    moveSound = p.mixer.Sound('sounds/move.wav')
    gameState = Engine.GameState()
    moveMade = False
    validMoves = gameState.getValidMoves()
    #load images only once
    loadImages()
    running = True
    selectedSquare = () # tracks last move
    playerClicks = [] # count mouseclicks
    animate = True
    gameOver = False
    rainbowColors = [(153,0,153), (111,0,255), (0,0,255), (0,204,0), (255,255,0),  (255,128,0),  (255,0,0)]
    endScreenFrameCount = 0
    playerOne = True # True if human, flase if AI, white
    playerTwo = False # black
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
                                # TODO see if its pawnpromotion and ask for choice
                                break
                        if not moveMade:
                            playerClicks = [selectedSquare]
            # key handler
            if e.type == p.KEYDOWN:
                if e.key == p.K_r:
                    gameState.undoMove()
                    moveMade = True
                    animate = False
                    gameOver = False
                if e.key == p.K_n:
                    gameState = Engine.GameState()
                    validMoves = gameState.getValidMoves()
                    selectedSquare = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
                    gameOver = False

        # AI choosing a move
        if not gameOver and not humanTurn:            
            AIMove = ChessAI.findBestMove(gameState, validMoves)
            if AIMove is None:
                AIMove = ChessAI.findRandomMove(validMoves)
            gameState.makeMove(AIMove)
            moveMade = True
            animate = True

        if moveMade:
            moveSound.play()
            if animate:
                animateMove(gameState.moveLog[-1], screen, gameState.board, clock)            
            if gameState.lateGameWeight >= 0.05:
                gameState.lateGameWeight -= 0.05
            validMoves = gameState.getValidMoves()
            moveMade = False
            animate = False     

        drawGameState(screen, gameState, validMoves, selectedSquare)

        if gameState.checkMate or gameState.staleMate:
            gameOver = True
            endScreenFrameCount = endScreenFrameCount + 1
            displayGameOverText(screen, gameState, endScreenFrameCount,rainbowColors)
        

        clock.tick(MAX_FPS)
        p.display.flip()


def displayGameOverText(screen, gameState, endScreenFrameCount,rainbowColors):
    index = (endScreenFrameCount % 70) // 10 - 1
    color = p.Color(rainbowColors[index][0],rainbowColors[index][1],rainbowColors[index][2])
    if gameState.checkMate:
        gameOver = True
        if gameState.whiteToMove:
            drawEndGameText(screen, "Black won!",color)
        if not gameState.whiteToMove:
            drawEndGameText(screen, "White won!",color)
    if gameState.staleMate:
        gameOver = True
        drawEndGameText(screen, "Draw!",color)
       

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



def drawGameState(screen, gameState, validMoves, selectedSquare):
    drawBoard(screen)
    highlightSquares(screen, gameState, validMoves, selectedSquare)
    drawPieces(screen, gameState.board)

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
    # TODO highlight the last move made

def drawEndGameText(screen, text, fontColor):
    font = p.font.SysFont("Helvitca", 64, True, False)
    textObject = font.render(text, 0, fontColor)
    textLocation = p.Rect(0,0, WIDTH, HEIGHT).move(WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)

# TODO add sound effects to the moves and checks




if __name__ == "__main__":
    main()

