""" Will stare all classes relevant to basic playing functionality
 to import to the main section. More and more feel I need to make a
piece object """


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
            ["--", "--", "--", "bQ", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.white_to_move = True

        # Eventually should make this only one list and have them derive
        # player list from log
        self.move_log = []  # The computer reads this for going its logic
        self.player_move_log = []   # This is what the player gets shown

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

    def get_all_moves(self):
        """ get list of all moves without worrying about checks """
        possible_moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                piece = self.board[r][c]

                if (piece[0] == "b" and self.white_to_move is False) or (piece[0] == "w" and self.white_to_move is True):
                    if piece[1] == "P":
                        for m in self.get_pawn_moves(r, c, piece):
                            possible_moves.append(m)
                    elif piece[1] == "R":
                        for m in self.get_rook_moves(r, c, piece):
                            possible_moves.append(m)
                    elif piece[1] == "N":
                        for m in self.get_knight_moves(r, c, piece):
                            possible_moves.append(m)
                    elif piece[1] == "B":
                        for m in self.get_bishop_moves(r, c, piece):
                            possible_moves.append(m)
                    elif piece[1] == "Q":
                        for m in self.get_queen_moves(r, c, piece):
                            possible_moves.append(m)
                    elif piece[1] == "K":
                        for m in self.get_king_moves(r, c, piece):
                            possible_moves.append(m)

        return possible_moves

    def get_legal_moves(self):
        """ fromt he above list, filter out moves that would put you in check """
        return self.get_all_moves()
    
    """ big set of moves here for piece specific logic"""
    def get_pawn_moves(self, r, c, piece):
        pawn_moves = []
        if piece[0] == "w":
            # Moving forwards
            if self.board[r-1][c] == "--":
                pawn_moves.append(Move([(r, c), (r-1, c)], self))
                if self.board[r-2][c] == "--" and r == 6:
                    pawn_moves.append(Move([(r, c), (r-2, c)], self))

            # Captures
            try:
                if self.board[r-1][c-1][0] == "b":
                    pawn_moves.append(Move([(r, c), (r-1, c-1)], self))
                if self.board[r-1][c+1][0] == "b":
                    pawn_moves.append(Move([(r, c), (r-1, c+1)], self))
            except IndexError:
                pass
        
        return pawn_moves
                

    def get_rook_moves(self, r, c, piece):
        return []

    def get_knight_moves(self, r, c, piece):
        return []

    def get_bishop_moves(self, r, c, piece):
        return []

    def get_queen_moves(self, r, c, piece):
        return []

    def get_king_moves(self, r, c, piece):
        return []


class Move():
    """The properties of a move, so position in various expressions"""

    # These are just gunna be used moving things in and out fo chess notation
    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4,
                     "5": 3, "6": 2, "7": 1, "8": 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3,
                     "e": 4, "f": 5, "g": 6, "h": 7}
    cols_to_files = {v: k for k, v in files_to_cols.items()}

    # We'll call these a lot, let's make them less ugly
    def __init__(self, move, gs):
        self.start_row = move[0][0]
        self.start_column = move[0][1]
        self.end_row = move[1][0]
        self.end_column = move[1][1]
        self.start_piece = gs.board[self.start_row][self.start_column]
        self.end_piece = gs.board[self.end_row][self.end_column]
        self.record = (self.start_piece, self.start_row, self.start_column, self.end_piece, self.end_row, self.end_column)

    def __eq__(self, other):
        """ method to check whether two moves are equal """
        if isinstance(other, Move):
            return self.record == other.record
        return False

    def __str__(self):
        """ what gets shown when we print the object """
        return self.chess_notation()

    def chess_notation(self):
        """converts the move as python sees it to standard chess notation for log
        can't do castling, promotion, or check atm"""
        notation = ""
        if "P" not in self.start_piece:
            notation += self.start_piece[1]
        # Below line should only be used when there's ambiguity about what piece
        # could have moved. That's hard to detect atm
        # notation += self.get_rank_file(self.start_row, self.start_column)
        if self.end_piece != "--":
            notation += "x"
        notation += self.get_rank_file(self.end_row, self.end_column)
        return notation

    def get_rank_file(self, r, c):
        """Converts our row column system to how chess notation
        should actually look"""
        return self.cols_to_files[c] + self.rows_to_ranks[r]
