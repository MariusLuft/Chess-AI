# handles user input and displayes the current game state # 

import pygame as p
import Engine

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
    gameState = Engine.GameState()
    moveMade = False
    validMoves = gameState.getValidMoves()
    #load images only once
    loadImages()
    running = True
    selectedSquare = () # tracks last move
    playerClicks = [] # count mouseclicks
    animate = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # TODO Better game ending
            if gameState.checkMate or gameState.staleMate:
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
                    if not moveMade:
                        playerClicks = [selectedSquare]
            # key handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_r:
                    gameState.undoMove()
                    moveMade = True
                    animate = False
                if e.key == p.K_n:
                    gameState = Engine.GameState()
                    validMoves = gameState.getValidMoves()
                    selectedSquare = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
        if moveMade:
            if animate:
                animateMove(gameState.moveLog[-1], screen, gameState.board, clock)
            validMoves = gameState.getValidMoves()
            moveMade = False
            animate = False     

        clock.tick(MAX_FPS)
        p.display.flip()
        drawGameState(screen, gameState, validMoves, selectedSquare)

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
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        # draw moving pieces 
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)
    # TODO highlight the last move made



if __name__ == "__main__":
    main()

