class Move():
    """All things involving moving a piece, realised it will have bunch of methods"""

    # We'll call these a lot, let's make them less ugly
    def __init__(self, move, gs):
        self.start_row = move[0][0]
        self.start_column = move[0][1]
        self.end_row = move[1][0]
        self.end_column = move[1][1]
        self.start_piece = gs.board[self.start_row][self.start_column]
        self.end_piece = gs.board[self.end_row][self.end_column]

    def verify_move(self, move, gs):
        if self.start_piece != "--" and (self.start_row, self.start_column) != (self.end_row, self.end_column):
            gs.move_log.append(((self.start_row, self.start_column), self.start_piece),
                               ((self.end_row, self.end_column), self.end_piece))
            gs.board[move[1][0]][move[1][1]] = self.start_piece
            gs.board[move[0][0]][move[0][1]] = "--"
            gs.white_to_move = not gs.white_to_move
