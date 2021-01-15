import random
import chess
import chess.polyglot
import time

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

    # time.sleep(60)

    move_made = valid_moves[random.randint(0, len(valid_moves) - 1)]
    move_played_string = move_made.get_chess_notation()
    board.push(chess.Move.from_uci(move_played_string))
    print("Random Move")
    print("Move Made: " + move_played_string)
    print(board)
    print("--------------------------------------------------------------------------------")
    return move_made

# def find_better_move(valid_moves):


