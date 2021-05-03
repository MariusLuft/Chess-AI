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
        