# stores information about the current state of the board, and responsible for determining valid moves

class game_state():

    # constructor
    def __init__(self):

        # board represented by list of lists (8x8 board) 
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]

        # helper function definitions
        self.get_moves = {
            "P": self.get_pawn_moves, "R": self.get_rook_moves, 
            "B": self.get_bishop_moves, "N": self.get_knight_moves,
            "Q": self.get_queen_moves, "K": self.get_king_moves
        }

        self.in_check = False
        self.white_to_move = True

        self.move_log = []
        self.white_king_location = (7, 4)
        self.black_king_location = (0, 4)

        self.pins = []
        self.checks = []

    # execute move (does not work with pawn promotion, en passant or castling)
    def make_move(self, move):
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved    
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move

        if move.piece_moved == "wK":
            self.white_king_location = (move.end_row, move.end_col)
        elif move.piece_moved == "bK":
            self.black_king_location = (move.end_row, move.end_col)
    
    # undo last move made
    def undo_move(self, move):
        if(self.move_log != 0):
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured   
            self.move_log.pop()
            self.white_to_move = not self.white_to_move 

            if move.piece_moved == "wK":
                self.white_king_location = (move.end_row, move.end_col)
            elif move.piece_moved == "bK":
                self.black_king_location = (move.end_row, move.end_col)

    # helpers for getting moves for each piece 
    def get_pawn_moves(self, row, col, moves):

        # checking for pinned condition
        piece_pinned = False
        pin_direction = ()

        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        # can move one or two squares forward on first move, captures diagonally

        # white
        if self.white_to_move:

            if row > 0:
                # move forwards one and forwards two
                if self.board[row - 1][col] == "--":
                    if not piece_pinned or pin_direction == (-1, 0):
                        moves.append(move((row, col), (row - 1,col), self.board))
                        if row == 6 and self.board[row - 2][col] == "--":
                                moves.append(move((row, col), (row - 2, col), self.board))
                # capture diagonally
                if col > 0 and col < (len(self.board) - 1):
                    if self.board[row - 1][col - 1][0] == "b":
                        if not piece_pinned or pin_direction == (-1, -1):
                            moves.append(move((row, col), (row - 1, col - 1), self.board))
                    if self.board[row - 1][col + 1][0] == "b":
                        if not piece_pinned or pin_direction == (-1, 1):
                            moves.append(move((row, col), (row - 1, col + 1), self.board))

        # black
        elif not self.white_to_move:

            if row < (len(self.board) - 1):
                # move forwards one and forwards two
                if self.board[row + 1][col] == "--":
                    if not piece_pinned or pin_direction == (1, 0):
                        moves.append(move((row, col), (row + 1, col), self.board))
                        if row == 1 and self.board[row + 2][col] == "--":
                                moves.append(move((row, col), (row + 2, col), self.board))
                # captures diagonally
                if col > 0 and col < (len(self.board) - 1):
                    if self.board[row + 1][col - 1][0] == "w":
                        if not piece_pinned or pin_direction == (1, -1):
                            moves.append(move((row, col), (row + 1, col - 1), self.board))
                    if self.board[row + 1][col + 1][0] == "w":
                        if not piece_pinned or pin_direction == (1, 1):
                            moves.append(move((row, col), (row + 1, col + 1), self.board))

    def get_rook_moves(self, row, col, moves):
        
        # checking for pinned condition
        # piece_pinned = False
        # pin_direction = ()

        # for i in range(len(self.pins) - 1, -1, -1):
        #     if self.pins[i][0] == row and self.pins[i][1] == col:
        #         piece_pinned = True
        #         pin_direction = (self.pins[i][2], self.pins[i][3])
        #         # can't remove queens from pin list
        #         if self.board[row][col][1] != "Q":
        #             self.pins.remove(self.pins[i])
        #         break

        # can move in straight line along files and ranks

        directions = ((-1, 0), (1, 0), (0, -1), (0, 1))
        enemy = "b" if self.white_to_move else "w"

        for d in directions:
            for i in range(1, 8):
                end_row = row + d[0] * i
                end_col = col + d[1] * i

                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]

                    if end_piece == "--":
                        moves.append(move((row, col), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy:
                        moves.append(move((row, col), (end_row, end_col), self.board))
                        break
                    else:
                        break
                else:
                    break

    def get_knight_moves(self, row, col, moves):
        
        # # checking for pinned condition
        # piece_pinned = False

        # for i in range(len(self.pins) - 1, -1, -1):
        #     if self.pins[i][0] == row and self.pins[i][1] == col:
        #         piece_pinned = True
        #         self.pins.remove(self.pins[i])
        #         break

        # can move in L shapes

        directions = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        ally = "w" if self.white_to_move else "b"

        for d in directions:
            end_row = row + d[0]
            end_col = col + d[1]

            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally:
                    moves.append(move((row, col) , (end_row, end_col), self.board))

    def get_bishop_moves(self, row, col, moves):
               
        # # checking for pinned condition
        # piece_pinned = False
        # pin_direction = ()

        # for i in range(len(self.pins) - 1, -1, -1):
        #     if self.pins[i][0] == row and self.pins[i][1] == col:
        #         piece_pinned = True
        #         pin_direction = (self.pins[i][2], self.pins[i][3])
        #         self.pins.remove(self.pins[i])
        #         break

        # can move in straight line along diagonals

        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemy = "b" if self.white_to_move else "w"
            
        for d in directions:
            for i in range(1, 8):
                
                end_row = row + d[0] * i
                end_col = col + d[1] * i

                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col] 

                    if end_piece == "--":
                        moves.append(move((row, col), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy:
                        moves.append(move((row, col), (end_row, end_col), self.board))
                        break
                    else:
                        break
                else:
                    break   

    def get_queen_moves(self, row, col, moves):
        self.get_bishop_moves(row, col, moves)
        self.get_rook_moves(row, col, moves)

    def get_king_moves(self, row, col, moves):
        
        directions = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        ally = "w" if self.white_to_move else "b"

        for i in range(1, 8):
            end_row = row + directions[i][0] 
            end_col = col + directions[i][1] 

            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]

                if end_piece != ally:
                    moves.append(move((row, col), (end_row, end_col), self.board))

    # get all valid moves (when in check)
    def valid_moves_checked(self):
        
        moves = []
        self.in_check, self.pins, self.checks = self.check_pins_checks()
        
        if self.white_to_move:
            king_row = self.white_king_location[0]
            king_col = self.white_king_location[1]
        else:
            king_row = self.black_king_location[0]
            king_col = self.black_king_location[1]
        
        # if in check
        if self.in_check:

            # one check (block this check or move king to valid square)
            if len(self.checks) == 1:
                moves = self.valid_moves()
                
                # block
                valid_squares = [] #squares that can be occupied to block
                check = self.checks[0]
                check_row = check[0]
                check_col = check[1]
                checking_piece = self.board[check_row][check_col]

                # if knight, must capture knight (cannot block)
                if checking_piece[1] == "N":
                    valid_squares = [(check_row, check_col)]
                
                # go through to see which squares are valid to be able to block
                else:
                    for i in range(1,8):
                        valid_square = (king_row + check[2] * i, king_col + check[3] * i)
                        valid_squares.append(valid_square)
                        if valid_square[0] == check_row and valid_square[1] == check_col:
                            break
                
                # remove moves that don't block check or move king location
                for i in range(len(moves) - 1, -1, -1):
                    if moves[i].piece_moved[1] != "K":
                        if (moves[i].end_row, moves[i].end_col) not in valid_squares:
                            moves.remove(moves[i])

            # else two checks, must move king
            else:
                self.get_king_moves(king_row, king_col, moves)

        # else not in check
        else:
            moves = self.valid_moves()

        return moves
    
    # get all valid moves
    def valid_moves(self):
        moves = []

        # parse through the board now to check for each piece and its possible moves
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                colour = self.board[row][col][0]
                if (colour == "w" and self.white_to_move or colour == "b" and not self.white_to_move):
                    piece = self.board[row][col][1]
                    self.get_moves[piece](row, col, moves)
 
        return moves

    # checks for pins and checks
    def check_pins_checks(self):
        
        pins = [] # refers to pinned allied pieces
        checks = [] # refers to enemy pieces putting king in check
        in_check = False
        
        if self.white_to_move:
            ally = "w"
            enemy = "b"
            king_row = self.white_king_location[0]
            king_col = self.white_king_location[1]
        else:
            ally = "b"
            enemy = "w"
            king_row = self.black_king_location[0]
            king_col = self.black_king_location[1]
 
        # check outward in all eight directions for pins and checks
        directions = ((-1, 0), (0, -1), (0, 1), (1, 0), (-1,-1), (-1, 1), (1, 1), (1, -1))
        
        for j in range(len(directions)):
            d = directions[j]
            possible_pin = ()
            for i in range(1, 8):
                end_row = king_row + d[0] * i
                end_col = king_col + d[1] * i

                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]

                    if end_piece[0] == ally and end_piece[1] != "K":
                        if possible_pin == ():
                            # save the location of the pin and the direction to the king
                            possible_pin = (end_row, end_col, d[0], d[1])
                        else:
                            break
                    
                    elif end_piece[0] == enemy:
                        piece = end_piece[1]
                        # possible cases for an attacking piece
                        if (0 <= j < 4 and piece == "R") or \
                            (4 <= j < 8 and piece == "B") or \
                            (i == 1 and piece == "P" and ((enemy == "w" and 4 <= j <= 5) or (enemy == "b" and 6 <= j <=7))) or \
                            (piece == "Q") or (i == 1 and piece == "K"):
                            if possible_pin == ():
                                in_check == True
                                checks.append(end_row, end_col, d[0], d[1])
                            else:
                                pins.append(possible_pin)
                                break
                        else:
                            break
                else:
                    break

        knight_directions = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for k in knight_directions:
            end_row = king_row + k[0]
            end_col = king_col + k[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] == enemy and end_piece[1] == "N":
                    in_check = True
                    checks.append((end_row, end_col, k[0], k[1]))
            else:
                break 
        
        return pins, checks, in_check

class move():

    # chess notation transcription
    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    cols_to_files = {v: k for k, v in files_to_cols.items()}

    def __init__(self, start_pos, end_pos, board):
        
        # coordinates for start and end positions
        self.start_row = start_pos[0]
        self.start_col = start_pos[1]
        self.end_row = end_pos[0]
        self.end_col = end_pos[1]

        # pieces moved and captured
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
    
        # move id
        self.move_id = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col

    # not actually chess notation
    def get_chess_notation(self):
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)

    # get coordinates
    def get_rank_file(self, row, col):
        return self.cols_to_files[col] + self.rows_to_ranks[row]

    # cannot use the regular == comparator, we need to override this
    def __eq__(self, other):
        # first check that other is an actual Move class object
        if isinstance(other, move):
            if self.move_id == other.move_id:
                return True
            else:
                 return False