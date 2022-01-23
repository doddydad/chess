class Game_State():
    """
This class stores all information about the gamestate

changes for later, change board storage to numpy array for speed
"""

    def __init__(self):
        # Board is 8x8 list, each element having 2 characters,[colour, piece]
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.white_to_move = True
        self.move_log = []

    def make_move(self, move):
        """Changing the positions on the actual board"""
        self.move_log.append(move.chess_notation())
        self.board[move.end_row][move.end_column] = move.start_piece
        self.board[move.start_row][move.start_column] = "--"
        self.white_to_move = not self.white_to_move

    def verify_move(self, move):
        """ Will be long function to check if a move is legal"""
        if move.start_piece[0] != "w" and self.white_to_move is True:
            return False
        elif move.start_piece[0] != "b" and self.white_to_move is False:
            return False
        return True
