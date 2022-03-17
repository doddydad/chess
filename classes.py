""" Will stare all classes relevant to basic playing functionality
 to import to the main section. I cna see how you could make piece types
each a separate class inheriting from piece but I felt this was tidier """


class Game_State():
    """
This class stores all information about the gamestate

changes for later, change board storage to numpy array for speed
"""

# Currently can't do castling, promotion or en passant

    def __init__(self):
        # Board is 8x8 list, each being an object with a colour value given
        self.board = [
            [Rook("b"), Knight("b"), Bishop("b"), Queen("b"), King("b"), Bishop("b"), Knight("b"), Rook("b")],
            [Pawn("b"), Pawn("b"), Pawn("b"), Pawn("b"), Pawn("b"), Pawn("b"), Pawn("b"), Pawn("b")],
            [Piece("-"), Piece("-"), Piece("-"), Piece("-"), Piece("-"), Piece("-"), Piece("-"), Piece("-")],
            [Piece("-"), Piece("-"), Piece("-"), Piece("-"), Piece("-"), Piece("-"), Piece("-"), Piece("-")],
            [Piece("-"), Piece("-"), Piece("-"), Piece("-"), Piece("-"), Piece("-"), Piece("-"), Piece("-")],
            [Piece("-"), Piece("-"), Piece("-"), Piece("-"), Piece("-"), Piece("-"), Piece("-"), Piece("-")],
            [Pawn("w"), Pawn("w"), Pawn("w"), Pawn("w"), Pawn("w"), Pawn("w"), Pawn("w"), Pawn("w")],
            [Rook("w"), Knight("w"), Bishop("w"), Queen("w"), King("w"), Bishop("w"), Knight("w"), Rook("w")]]
        self.white_to_move = True

        # Eventually should make this only one list and have them derive
        # player list from log
        self.move_log = []  # The computer reads this for going its logic
        self.player_move_log = []   # This is what the player gets shown

        # Allows you dictionary of move types

    def make_move(self, move):
        """Changing the positions on the actual board"""
        self.move_log.append(move)
        self.player_move_log.append(move.chess_notation())
        self.board[move.end_row][move.end_column] = move.start_piece
        self.board[move.end_row][move.end_column].moved = True
        self.board[move.start_row][move.start_column] = Piece("-")
        self.white_to_move = not self.white_to_move

    def undo_move(self):
        """ Undoes the most recent game move"""
        # Getting the last move and removing it from the records
        if self.move_log:
            last_move = self.move_log.pop()
            self.player_move_log = self.player_move_log[:-1]
            # Undoing the move
            self.board[last_move.start_row][last_move.start_column] = last_move.start_piece
            self.board[last_move.start_row][last_move.start_column].moved = last_move.start_moved
            self.board[last_move.end_row][last_move.end_column] = last_move.end_piece
            self.white_to_move = not self.white_to_move

    def get_all_moves(self):
        """ get list of all moves without worrying about checks """
        possible_moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                p = self.board[r][c]
                try:
                    for m in p.move(r, c, self):
                        possible_moves.append(m)
                except TypeError:
                    pass

        return possible_moves

    def get_legal_moves(self):
        """ from the above list, filter out moves that would put you in check """
        legal_moves = []
        for m in self.get_all_moves():
            legal = True
            self.make_move(m)
            potential_moves = self.get_all_moves()
            for m_2 in potential_moves:
                if m_2.end_piece.type == "King":
                    legal = False
            if legal:
                legal_moves.append(m)
            self.undo_move()
        return legal_moves

    # goals, simulate the move, get list of valid moves, if any are king captures
    # remove that move from the list

    """ big set of moves here for piece specific logic"""


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
        self.start_moved = self.start_piece.moved
        self.record = (self.start_row, self.start_column, self.end_row,
                       self.end_column, self.start_piece, self.end_piece,
                       self.start_moved)

    def __eq__(self, other):
        """ method to check whether two moves are equal """
        if isinstance(other, Move):
            return self.record == other.record
        return False

    def __str__(self):
        """ what gets shown when we print the object """
        return self.chess_notation()

    def chess_notation(self):
        """converts the move as python sees it to standard chess notation for
        log can't do castling, promotion, or check atm"""
        notation = ""
        if "P" != self.start_piece.type[0]:
            notation += self.start_piece.type
        # Below line should only be used when there's ambiguity about what
        # piece could have moved. That's hard to detect atm
        # notation += self.get_rank_file(self.start_row, self.start_column)
        if self.end_piece.colour != "-":
            notation += "x"
        notation += self.get_rank_file(self.end_row, self.end_column)
        return notation

    def get_rank_file(self, r, c):
        """Converts our row column system to how chess notation
        should actually look"""
        return self.cols_to_files[c] + self.rows_to_ranks[r]


class Piece():
    """ Contains the attributes of a piece, position though will be saved in
    gamestate """

    def __init__(self, colour):
        self.colour = colour
        self.type = ""
        self.picture = "--"
        self.moved = False

    def __str__(self):
        return self.picture

    def __eq__(self, other):
        if isinstance(other, Piece):
            return self.picture == other.picture
        return False

    def move(self, r, c, gs):
        return []


""" All pieces inherit from strings with just some logic to find moves and
assign names and values """


class Queen(Piece):
    """ Specifics for the queen"""

    def __init__(self, colour):
        super().__init__(self)
        self.type = "Queen"
        self.picture = colour + "Q"
        self.colour = colour
        self.value = 9

    def move(self, r, c, gs):
        """Creates moves for a queen"""
        moves = []
        for m in Rook.move(self, r, c, gs):
            moves.append(m)
        for m in Bishop.move(self, r, c, gs):
            moves.append(m)

        return moves


class Rook(Piece):
    """ Specifics for the queen"""

    def __init__(self, colour):
        super().__init__(self)
        self.type = "Rook"
        self.picture = colour + "R"
        self.colour = colour
        self.value = 5

    def move(self, r, c, gs):
        """ creates the possible moves for the rook"""
        moves = []
        if self.colour == "b" and gs.white_to_move or self.colour == "w" and not gs.white_to_move:
            return moves

        for x in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
            i = 1
            while 0 <= r+(i*x[0]) < 8 and 0 <= c+(i*x[1]) < 8:
                end_row = r+(i*x[0])
                end_col = c+(i*x[1])
                if gs.board[end_row][end_col].colour != self.colour:
                    moves.append(Move([(r, c), (end_row, end_col)], gs))
                    if gs.board[end_row][end_col].colour != "-":
                        break
                    i += 1
                else:
                    break
        return moves


class Knight(Piece):
    """ Specifics for the knight"""

    def __init__(self, colour):
        super().__init__(self)
        self.type = "Night"
        self.picture = colour + "N"
        self.colour = colour
        self.value = 3

    def move(self, r, c, gs):
        """ If piece being tested is a knight, this returns its moves"""
        # Should be complete
        moves = []
        if self.colour == "b" and gs.white_to_move or self.colour == "w" and not gs.white_to_move:
            return moves

        for x in [[2, 1], [2, -1], [-2, 1], [-2, -1], [1, 2], [1, -2],
                  [-1, 2], [-1, -2]]:
            end_row = r+x[0]
            end_col = c+x[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                if gs.board[end_row][end_col].colour != self.colour:
                    moves.append(Move([(r, c), (end_row, end_col)], gs))

        return moves


class Bishop(Piece):
    """ Specifics for the bishop"""

    def __init__(self, colour):
        super().__init__(self)
        self.type = "Bishop"
        self.picture = colour + "B"
        self.colour = colour
        self.value = 3

    def move(self, r, c, gs):
        """ If piece being tested is a bishop, this returns its moves"""
        moves = []
        if self.colour == "b" and gs.white_to_move or self.colour == "w" and not gs.white_to_move:
            return moves

        for x in [[1, 1], [1, -1], [-1, -1], [-1, 1]]:
            i = 1
            while 0 <= r+(i*x[0]) < 8 and 0 <= c+(i*x[1]) < 8:
                end_row = r+(i*x[0])
                end_col = c+(i*x[1])
                if gs.board[end_row][end_col].colour != self.colour:
                    moves.append(Move([(r, c), (end_row, end_col)], gs))
                    if gs.board[end_row][end_col].colour != "-":
                        break
                    i += 1
                else:
                    break

        return moves


class Pawn(Piece):
    """ Specifics for the queen"""

    def __init__(self, colour):
        super().__init__(self)
        self.type = "Pawn"
        self.picture = colour + "P"
        self.colour = colour
        self.value = 1

    def move(self, r, c, gs):
        """If the piece being tested is a pawn, this finds its moves"""
        moves = []
        if self.colour == "b" and gs.white_to_move or self.colour == "w" and not gs.white_to_move:
            return moves

        if self.colour == "w":
            # Moving forwards
            if gs.board[r-1][c].colour == "-":
                moves.append(Move([(r, c), (r-1, c)], gs))
                if gs.board[r-2][c].colour == "-" and r == 6:
                    moves.append(Move([(r, c), (r-2, c)], gs))

            # Captures
            if c - 1 >= 0:
                if gs.board[r-1][c-1].colour == "b":
                    moves.append(Move([(r, c), (r-1, c-1)], gs))
            if c + 1 < 8:
                if gs.board[r-1][c+1].colour == "b":
                    moves.append(Move([(r, c), (r-1, c+1)], gs))


        if self.colour == "b":
            # Moving forwards
            if gs.board[r+1][c].colour == "-":
                moves.append(Move([(r, c), (r+1, c)], gs))
                if gs.board[r+2][c].colour == "-" and r == 1:
                    moves.append(Move([(r, c), (r+2, c)], gs))

            # Captures
            if c - 1 >= 0:
                if gs.board[r+1][c-1].colour == "w":
                    moves.append(Move([(r, c), (r+1, c-1)], gs))
            if c + 1 < 8:
                if gs.board[r+1][c+1].colour == "w":
                    moves.append(Move([(r, c), (r+1, c+1)], gs))

        return moves

    def promote(self, r, c, gs):
        pass

class King(Piece):
    """ Specifics for the king"""

    def __init__(self, colour):
        super().__init__(self)
        self.type = "King"
        self.picture = colour + "K"
        self.colour = colour
        self.value = 9999

    def move(self, r, c, gs):
        moves = []
        if self.colour == "b" and gs.white_to_move or self.colour == "w" and not gs.white_to_move:
            return moves

        for x in [[1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0],
                  [-1, 1], [0, 1]]:
            if 0 <= (r + x[0]) < 8 and 0 <= (c + x[1]) < 8:
                if gs.board[r+x[0]][c+x[1]].colour != self.colour:
                    moves.append(Move([(r, c), (r+x[0], c+x[1])], gs))

        return moves
