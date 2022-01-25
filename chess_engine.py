class Game_State():
    """
This class stores all information about the gamestate

changes for later, change board storage to numpy array for speed
"""

# Currently can't do castling, promotion or en passant

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
        self.move_log = []  # The computer reads this for going its logic
        self.player_move_log = []   # This is what the player gets shown
        self.temp = []

    def make_move(self, move):
        """Changing the positions on the actual board"""
        self.move_log.append(move)
        self.player_move_log.append(move.chess_notation())
        self.board[move.end_row][move.end_column] = move.start_piece
        self.board[move.start_row][move.start_column] = "--"
        self.white_to_move = not self.white_to_move

    def undo_move(self):
        """ Undoes the mos recent game move"""
        # Getting the last move and removing it from the records
        if self.move_log:
            last_move = self.move_log.pop()
            self.player_move_log = self.player_move_log[:-1]
            # Undoing the move
            self.board[last_move.start_row][last_move.start_column] = last_move.start_piece
            self.board[last_move.end_row][last_move.end_column] = last_move.end_piece
            self.white_to_move = not self.white_to_move

    def gen_legal_moves(self):
        """ Generate a list of valid moves """
        for row in self.board:
            for piece in row:
                if "b" in piece:
                    pass
        
