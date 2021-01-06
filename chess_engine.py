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
        # print(move.move_id)
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move

        if move.piece_moved == "wK":
            self.white_king_location = (move.end_row, move.end_col)
        elif move.piece_moved == "bK":
            self.black_king_location = (move.end_row, move.end_col)
    
    # undo last move made
    def undo_move(self, move):
        if(self.move_log != 0):
            # print(move.move_id)
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured   
            self.move_log.pop()
            self.white_to_move = not self.white_to_move 
            # print(self.move_log)   

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
        piece_pinned = False
        pin_direction = ()

        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                # can't remove queens from pin list
                if self.board[row][col][1] != "Q":
                    self.pins.remove(self.pins[i])
                break

        # can move in straight line along files and ranks

        # white or black
        colour = "w" if self.white_to_move else "b"

        # horizontally
        for square in range(len(self.board)):
            
            valid = True
            
            if square == col:
                continue
            
            if self.board[row][square][0] != colour:
                # verify that there are no pieces blocking path
                if square < col:
                    for c in range(square + 1, col):
                        if self.board[row][c] != "--":
                            valid = False
                elif square > col:
                    for c in range(col + 1, square):
                        if self.board[row][c] != "--":
                            valid = False
                if valid and not piece_pinned or pin_direction == (0, 1) or pin_direction == (0,-1):
                    moves.append(move((row, col), (row, square), self.board))
        

        # vertically
        for square in range(len(self.board)):
            
            valid = True
        
            if square == row:
                continue

            if self.board[square][col][0] != colour:
                # verify that there are no pieces blocking path
                if square < row:
                    for r in range(square + 1, row):
                        if self.board[r][col] != "--":
                            valid = False
                elif square > row:
                    for r in range(row + 1, square):
                        if self.board[r][col] != "--":
                            valid = False
                if valid and not piece_pinned or pin_direction == (-1, 0) or pin_direction == (1,0):
                    moves.append(move((row, col), (square, col), self.board))

    def get_knight_moves(self, row, col, moves):
        
        # checking for pinned condition
        piece_pinned = False

        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                self.pins.remove(self.pins[i])
                break

        # can move in L shapes

        # colour
        colour = "w" if self.white_to_move else "b"


        # upwards tall L's
        if row >= 2: 
            if col < (len(self.board) - 1):
                if self.board[row - 2][col + 1][0] != colour and not piece_pinned:
                    moves.append(move((row, col), (row - 2, col + 1), self.board))
            if col > 0:
                if self.board[row - 2][col - 1][0] != colour and not piece_pinned:
                    moves.append(move((row, col), (row - 2, col - 1), self.board))
        
        # downwards tall L's
        if row < (len(self.board) - 2):
            if col < (len(self.board) - 1):
                if self.board[row + 2][col + 1][0] != colour and not piece_pinned:
                    moves.append(move((row, col), (row + 2, col + 1), self.board))
            if col > 0:
                if self.board[row + 2][col - 1][0] != colour and not piece_pinned:
                    moves.append(move((row, col), (row + 2, col - 1), self.board))
        
        # upwards sideways L's
        if row >= 1:
            if col < (len(self.board) - 2):
                if self.board[row - 1][col + 2][0] != colour and not piece_pinned:
                    moves.append(move((row, col), (row - 1, col + 2), self.board))
            if col > 1:
                if self.board[row - 1][col - 2][0] != colour and not piece_pinned:
                    moves.append(move((row, col), (row - 1, col - 2), self.board))
            
        # downwards sideways L's
        if row < (len(self.board) - 1):
            if col >= 2:
                if self.board[row + 1][col - 2][0] != colour and not piece_pinned:
                    moves.append(move((row, col), (row + 1, col - 2), self.board))
            if col < (len(self.board) - 2):
                if self.board[row + 1][col + 2][0] != colour and not piece_pinned:
                    moves.append(move((row, col), (row + 1, col + 2), self.board))

    def get_bishop_moves(self, row, col, moves):
               
        # checking for pinned condition
        piece_pinned = False
        pin_direction = ()

        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        # can move in straight line along diagonals

        # white or black
        colour_capt = "b" if self.white_to_move else "w"
            
        r1 = row - 1
        r2 = row + 1
        c1 = col - 1
        c2 = col + 1

        top_l_path = True
        top_r_path = True
        bottom_l_path = True
        bottom_r_path = True

        while top_l_path or top_r_path or bottom_r_path or bottom_l_path:
            
            # bounds check
            if r1 < 0:
                r1 = 0
                top_l_path = False
                top_r_path = False
            if r2 > (len(self.board) - 1):
                r2 = 7
                bottom_l_path = False
                bottom_r_path = False
            if c1 < 0:
                c1 = 0
                top_l_path = False
                bottom_l_path = False
            if c2 > (len(self.board) - 1):
                c2 = 7
                top_r_path = False
                bottom_r_path = False
            
            # TOP

            # top left diag capture 
            if top_l_path and self.board[r1][c1][0] == colour_capt:
                if not piece_pinned or pin_direction == (-1, -1):
                    moves.append(move((row, col), (r1, c1), self.board))
                    top_l_path = False

            # top left diag normal
            if top_l_path and self.board[r1][c1] == "--":
                if not piece_pinned or pin_direction == (-1, -1):
                    moves.append(move((row, col), (r1, c1), self.board))

            # top right diag capture
            if top_r_path and self.board[r1][c2][0] == colour_capt:
                if not piece_pinned or pin_direction == (-1, 1):
                    moves.append(move((row, col), (r1, c2), self.board))
                    top_r_path = False
                
            # top right diag normal
            if top_r_path and self.board[r1][c2] == "--":
                if not piece_pinned or pin_direction == (-1, 1):
                    moves.append(move((row, col), (r1, c2), self.board))

            # BOTTOM

            # bottom left diag capture
            if bottom_l_path and self.board[r2][c1][0] == colour_capt:
                if not piece_pinned or pin_direction == (1, -1):
                    moves.append(move((row, col), (r2, c1), self.board))
                    bottom_l_path = False

            # bottom left diag normal
            if bottom_l_path and self.board[r2][c1] == "--":
                if not piece_pinned or pin_direction == (1, -1):
                    moves.append(move((row, col), (r2, c1), self.board))

            # bottom right diag capture
            if bottom_r_path and self.board[r2][c2][0] == colour_capt:
                if not piece_pinned or pin_direction == (1, 1):
                    moves.append(move((row, col), (r2, c2), self.board))
                    bottom_r_path = False
                
            # bottom right diag normal
            if bottom_r_path and self.board[r2][c2] == "--":
                if not piece_pinned or pin_direction == (1, 1):
                    moves.append(move((row, col), (r2, c2), self.board))
            
            r1 -= 1
            c1 -= 1
            r2 += 1
            c2 += 1

    def get_queen_moves(self, row, col, moves):
        self.get_bishop_moves(row, col, moves)
        self.get_rook_moves(row, col, moves)

    def get_king_moves(self, row, col, moves):
        
        colour = "w" if self.white_to_move else "b"
        
        # try using try and except
    
        try:
            if self.board[row - 1][col - 1][0] != colour:
                self.king_helper(row, col, row - 1, col - 1, colour, moves)
        except:
            pass

        try: 
            if self.board[row - 1][col][0] != colour:
                self.king_helper(row, col, row - 1, col, colour, moves)
        except:
            pass

        try: 
            if self.board[row - 1][col + 1][0] != colour:
                self.king_helper(row, col, row - 1, col + 1, colour, moves)
        except:
            pass

        try: 
            if self.board[row + 1][col - 1][0] != colour:
                self.king_helper(row, col, row + 1, col - 1, colour, moves)
        except:
            pass

        try: 
            if self.board[row + 1][col][0] != colour:
                self.king_helper(row, col, row + 1, col, colour, moves)
        except:
            pass

        try: 
            if self.board[row + 1][col + 1][0] != colour:
                self.king_helper(row, col, row + 1, col + 1, colour, moves)
        except:
            pass

        try:
            if self.board[row][col - 1][0] != colour:
                self.king_helper(row, col, row, col - 1, colour, moves)
        except:
            pass

        try:
            if self.board[row][col + 1][0] != colour:
                self.king_helper(row, col, row, col + 1, colour, moves)
        except:
            pass

    # king helper to check for valid king moves
    def king_helper(self, row, col, end_row, end_col, colour, moves):
        
        if colour == "w":
            self.white_king_location = (end_row, end_col)
        else:
            self.black_king_location = (end_row, end_col)

        in_check, pins, checks = self.check_pins_checks()

        if not in_check:
            moves.append((row, col, end_row, end_col, self.board))
        
        if colour == "w":
            self.white_king_location = (row, col)
        else:
            self.black_king_location = (row, col)

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
                        if not (moves[i].end_row, moves[i].end_col) in valid_squares:
                            moves.remove(moves[i])

            # else two checks, must move king
            else:
                self.get_king_moves(king_row, king_col, moves)

        # else not in check
        else:
            moves = self.valid_moves()
    
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

                try:
                    end_piece = self.board[end_row][end_col]

                    if end_piece[0] == ally:
                        if possible_pin == ():
                            # save the location of the pin and the direction to the king
                            possible_pin = (end_row, end_col, d[0], d[1])
                        else:
                            break
                    
                    elif end_piece[0] == enemy:
                        type = end_piece[1]
                        # possible cases for an attacking piece
                        if (0 <= j < 4 and type == "R") or \
                            (4 <= j < 8 and type == "B") or \
                            (i == 1 and type == "P" and ((enemy == "w" and 4 <= j <= 5) or (enemy == "b" and 6 <= j <=7))) or \
                            (type == "Q") or (i == 1 and type == "K"):
                            if possible_pin == ():
                                in_check == True
                                checks.append(end_row, end_col, d[0], d[1])
                            else:
                                pins.append(possible_pin)
                                break
                        else:
                            break
                except:
                    pass

        knight_directions = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for k in knight_directions:
            end_row = king_row + k[0]
            end_col = king_col + k[1]
            try:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] == enemy and end_piece[1] == "N":
                    in_check = True
                    checks.append((end_row, end_col, k[0], k[1]))
            except:
                pass 
        
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