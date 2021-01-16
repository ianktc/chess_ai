import random
import chess
import chess.polyglot
import time

piece_scores = {"K": 0, "Q": 10, "R": 5, "N": 3, "B": 3, "P": 1}
CHECKMATE = 1000
STALEMATEZ = 0

def find_random_move(valid_moves, gs, board):

    opening_move = 0
    weight = 0

    # if gs.white_to_move:
    # with chess.polyglot.open_reader("opening_book/poly17/books/Perfect2017-SF12.bin") as reader:
    #     for entry in reader.find_all(board):
    #         if entry.weight > weight:
    #             opening_move = str(entry.move)
    #             weight = entry.weight
    #         print(entry.move, entry.weight)

    with chess.polyglot.open_reader("opening_book/pwned.polyglot.bin") as reader:
        for entry in reader.find_all(board):
            if entry.weight > weight:
                opening_move = str(entry.move)
                weight = entry.weight
            print(entry.move, entry.weight)

    for move in valid_moves:

        if move.get_chess_notation() == opening_move:
            
            print("Book Used")
            print("Move Made: " + move.get_chess_notation())

            # update ascii board
            move_played_string = move.get_chess_notation()
            board.push(chess.Move.from_uci(move_played_string))
            print(board)
            print("--------------------------------------------------------------------------------")
            return move

    move_made = valid_moves[random.randint(0, len(valid_moves) - 1)]
    move_played_string = move_made.get_chess_notation()
    board.push(chess.Move.from_uci(move_played_string))
    print("Random Move")
    print("Move Made: " + move_played_string)
    print(board)
    print("--------------------------------------------------------------------------------")
    return move_made

def find_better_move(valid_moves, gs):
    
    turn = 1 if gs.white_to_move else -1

    max_score = -CHECKMATE
    best_move = None

    for player_move in valid_moves:
        gs.make_move(player_move)
        
        
        # add in checkmate and stalemate if conditions
        '''
        if gs.checkmate:
            score = CHECKMATE
        elif gs.stalemate:
            score = STALEMATE
        else:
        '''
        score = turn * score_material(gs.board)
        
        if score > max_score:
            max_score = score
            best_move = player_move

        gs.undo_move(player_move)

    return best_move

def score_material(board):

    total_score = 0

    # really negative score for black and really positive score for white

    for row in board:
        for col in row:
            if col[0] == "w":
                total_score += piece_scores[col[1]]
            elif col[0] == "b":
                total_score -= piece_scores[col[1]]

    return total_score

