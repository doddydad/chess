"""
Main driver file
Handles user input and displays the game state
"""

import logging
import pygame as p
import classes as c
p.init()

logging.basicConfig(filename="chess.log", level=logging.DEBUG)
logging.basicConfig(format='%(message)s')
# logging.debug(thing) to get it in the file to look at later

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT//DIMENSION
MAX_FPS = 15
IMAGES = {}


def load_images(set="basic"):
    """ Initialise a global dictionary of images. Will be called exactly once 
    in main"""
    # Creates dictionary where key accesses the appropriate image
    for piece in ["wP", "wR", "wN", "wB", "wK", "wQ", "bP", "bR", "bN", "bB",
                  "bK", "bQ"]:
        IMAGES[piece] = p.transform.scale(p.image.load("Images/" + set + "/"
                        + piece + ".png"), (SQ_SIZE, SQ_SIZE))

def draw_gamestate(screen, gs, move = []):
    """ draws everthing in modules so can switch out some stuff"""
    # Can later add parts to draw legal moves etc.
    draw_board(screen)  # Draws the squares
    draw_highlight(screen, move, gs)  # Highlights selected piece aand its moves
    draw_pieces(screen, gs)  # draws the pieces


def draw_board(screen):
    """Simply draw board, later might take inputs to customise the look"""
    colours = [p.Color("white"), p.Color("grey")]  # can potentially allow
    # these to be customised later

    for i in range(DIMENSION):
        for j in range(DIMENSION):
            p.draw.rect(screen, colours[(i+j) % 2], (i*SQ_SIZE, j*SQ_SIZE,
                                                     SQ_SIZE, SQ_SIZE))


def draw_highlight(screen, move, gs):
    """Draws a square to highlight the selected square"""
    # Broken atm
    if len(move) == 1:
        r = move[0][0]
        c = move[0][1]
        piece = gs.board[r][c]

        # highlights the square beneath the selected piece
        p.draw.rect(screen, p.Color("green"),
                    (c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

        # highlights possible squares to go to
        for m in gs.get_legal_moves():
            if m.start_row == r and m.start_column == c:
                m_c = m.end_column
                m_r = m.end_row
                p.draw.circle(screen, p.Color("yellow"),
                        ((m_c*SQ_SIZE) + SQ_SIZE//2, (m_r*SQ_SIZE) + SQ_SIZE//2),
                        SQ_SIZE//2)


def is_selection_valid(gs, square):
    """ Checks if the square selected contains a piece that can move """
    r = square[0]
    c = square[1]
    piece = gs.board[r][c]
    # logging.debug(f"Is_selection_valid called on {r} {c} {piece}")
    # logging.debug(f"piece colour is {piece.colour} and gs.white_to_move is {gs.white_to_move}")
        # logging.debug(f"first test succeeded on {r} {c} {piece}")

    for m in gs.get_legal_moves():
        if m.start_row == r and m.start_column == c:
            return True

    return False


def draw_pieces(screen, gs):
    """Draws the pieces, image choice handled in load_images"""
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            image = gs.board[row][column].picture
            if image != "--":  # that means empty
                screen.blit(IMAGES[image], p.Rect(column*SQ_SIZE,
                            row*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def main():
    """main loop for code, takes user input and changes the user side output"""
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    gs = c.Game_State()
    valid_moves = gs.get_legal_moves()
    # logging.debug(f"the valid moves are{gs.get_legal_moves()}")
    move_made = False  # Flag variable
    load_images()
    running = True
    player_clicks = []  # Places user has clicked

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

            # Getting input as regards moving pieces
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()  # gets (x,y) of mouse
                row = location[1]//SQ_SIZE
                column = location[0]//SQ_SIZE
                # Checks the first click is in a valid place
                if is_selection_valid(gs, (row, column)) or len(player_clicks) == 1:
                    player_clicks.append((row, column))
                # On the second click makes the move
                if len(player_clicks) >= 2:
                    move = c.Move(player_clicks, gs)
                    if move in valid_moves:
                        gs.make_move(move)
                        move_made = True
                        player_clicks = []
                        logging.debug(f"The move made was {move} and the next possible ones are")
                        for m in gs.get_legal_moves():
                            logging.debug(f"{m}")
                    else:
                        if is_selection_valid(gs, (row, column)):
                            player_clicks = [(row, column)]

            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undo_move()
                    move_made = True

        if move_made:
            valid_moves = gs.get_legal_moves()
            move_made = False

        clock.tick(MAX_FPS)
        p.display.flip()
        draw_gamestate(screen, gs, player_clicks)


if __name__ == "__main__":
    main()
