# stores information about the current state of the board, and responsible for determining valid moves

class game_state():
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
        self.white_to_move = True
        self.move_log = []
    
    # execute move (does not work with pawn promotion, en passant or castling)
    def make_move(self, move):
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved    
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move
    
    # undo last move made
    def undo_move(self, move):
        if(self.move_log != 0):
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured   
            self.move_log.pop()
            self.white_to_move = not self.white_to_move   

    # helpers for getting moves for each piece 
    def get_pawn_moves(self, row, col, moves):
        pass
    def get_rook_moves(self, row, col, moves):
        pass
    def get_knight_moves(self, row, col, moves):
        pass
    def get_bishop_moves(self, row, col, moves):
        pass
    def get_queen_moves(self, row, col, moves):
        pass
    def get_king_moves(self, row, col, moves):
        pass   

    # get all valid moves (when in check)
    def valid_moves_checked(self):
        return valid_moves()

    # get all valid moves
    def valid_moves(self):
        moves = [move((6,4), (4,4), self.board)]

        # parse through the board now to check for each piece and its possible moves
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                colour = self.board[row][col][0]
                if (colour == "w" and self.white_to_move or colour == "b" and not self.white_to_move):
                    piece = self.board[row][col][1]
                    
                    if piece == "P":
                        self.get_pawn_moves(row,col,moves)
                    elif piece == "R":
                        self.get_rook_moves(row,col,moves)
                    elif piece == "N":
                        self.get_knight_moves(row,col,moves)
                    elif piece == "B":
                        self.get_bishop_moves(row,col,moves)
                    elif piece == "Q":
                        self.get_queen_moves(row,col,moves)
                    elif piece == "K":
                        self.get_king_moves(row,col,moves)

        return moves

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