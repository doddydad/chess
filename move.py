class Move():
    """All things involving moving a piece, realised it will have bunch of
    methods"""

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
        