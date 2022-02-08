"""
Main driver file
Handles user input and displays the game state
"""

import logging
import pygame as p
import classes as c
p.init()

logging.basicConfig(filename="chess.log", level=logging.DEBUG)
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
    draw_highlight(screen, move)  # Highlights clicked square
    draw_pieces(screen, gs)  # draws the pieces


def draw_board(screen):
    """Simply draw board, later might take inputs to customise the look"""
    colours = [p.Color("white"), p.Color("grey")]  # can potentially allow
    # these to be customised later

    for i in range(DIMENSION):
        for j in range(DIMENSION):
            p.draw.rect(screen, colours[(i+j) % 2], (i*SQ_SIZE, j*SQ_SIZE,
                                                     SQ_SIZE, SQ_SIZE))


def draw_highlight(screen, move):
    """Draws a square to highlight the selected square"""
    if len(move) == 1:
        # highlights the square beneath the selected piece
        p.draw.rect(screen, p.Color("green"),
                    (move[0][1]*SQ_SIZE, move[0][0]*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def is_selection_valid(gs, square):
    """ Checks if the square selected contains a piece that can move """
    r = square[0]
    c = square[1]
    p = gs.board[r][c]
    if p.colour == "w" and gs.white_to_move is True or p.colour == "b" and gs.white_to_move is False:
        if gs.move_types[p.type](r, c, p):
            return gs.move_types[p.type](r, c, p)
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
    logging.debug(print(x) for x in valid_moves)
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
                column = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
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
                    else:
                        player_clicks = []

            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undo_move()
                    move_made = True

        if move_made:
            valid_moves = gs.get_legal_moves()
            logging.debug(valid_moves)
            move_made = False

        clock.tick(MAX_FPS)
        p.display.flip()
        draw_gamestate(screen, gs, player_clicks)


if __name__ == "__main__":
    main()
