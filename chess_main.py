# main driver responsible for handling user input and manipulating board state

import pygame as p 
import chess_engine

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15 # for animations
IMAGES = {} # dict for piece images

# init a global dict of images at the beginning of the game
def load_images():
    pieces = ["bR", "bN", "bB", "bQ", "bK", "bP", "wR", "wN", "wB", "wQ", "wK", "wP"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("pieces/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    
# main driver to handle user input and update the drawn board
def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))

    # construct board
    gs = chess_engine.game_state()

    # get valid moves
    valid_moves = gs.valid_moves()
    # flags when a valid move has been made, then generate a new set of valid_moves
    move_made = False 

    # print(gs.board)
    load_images()
    running = True

    # move
    initial_selection = ()
    final_selection = []

    while running:
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
            elif event.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                # if first click is same as most recent click then its a deselect
                if(initial_selection == (row, col)):
                    initial_selection = ()
                    final_selection = []
                # otherwise add it to the list of clicks
                else:
                    initial_selection = (row, col)
                    final_selection.append(initial_selection)
                # if most recent click diff than first click, its a move
                if(len(final_selection) == 2):
                    move = chess_engine.move(final_selection[0], final_selection[1], gs.board)

                    print(move.get_chess_notation())

                    if(move in valid_moves):
                        move_made = True
                        print(move.move_id)
                        gs.make_move(move)

                    # reset clicks
                    initial_selection = ()
                    final_selection = []

            elif event.type == p.KEYDOWN:
                if event.key == p.K_z:
                    gs.undo_move(move)
                    move_made = True

        if(move_made):
            move_made = False
            valid_moves = gs.valid_moves()

        draw_game_state(screen, gs)    
        clock.tick(MAX_FPS)
        p.display.flip()

# graphics for current game state
def draw_game_state(screen, gs):
    # draws the squares of board
    draw_squares(screen) 
    # draw pieces
    draw_pieces(screen, gs.board)

# helper for graphics (squares)
def draw_squares(screen):
    white = p.Color("white")
    grey = p.Color("grey")

    for row in range(DIMENSION):
        for col in range(DIMENSION):
            if((row + col) % 2 == 0):
                colour = white # colour white
            else:
                colour = grey # colour grey
            p.draw.rect(screen, colour, p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

# helper for graphics (pieces)
def draw_pieces(screen, board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if(piece != "--"):
                # look up blit usage after
                screen.blit(IMAGES[piece], p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE)) 

if __name__ == "__main__":
    main()