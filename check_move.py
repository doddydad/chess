class Move():
    """All things involving moving a piece, realised it will have bunch of methods"""

    # We'll call these a lot, let's make them less ugly
    def __init__(self, move, gs):
        start_row = move[0][0]
        start_column = move[0][1]
        end_row = move[1][0]
        end_column = move[1][1]
        start_piece = gs.board[move[0][0]][move[0][1]]
        end_piece = gs.board[move[1][0]][move[1][1]]

        if start_piece != "--" and (start_row, start_column) != (end_row, end_column):
            gs.move_log.append(((start_row, start_column), start_piece),
                               ((end_row, end_column), end_piece))
            gs.board[move[1][0]][move[1][1]] = start_piece
            gs.board[move[0][0]][move[0][1]] = "--"
            gs.white_to_move = not gs.white_to_move
