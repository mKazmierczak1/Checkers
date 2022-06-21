# constants which are specifying what is on a field on the game board
VOID = 0
PLAYER_1 = 1
PLAYER_2 = 2
PLAYER_1_KING = 3
PLAYER_2_KING = 4

# starting board
CHECKERS_LAYOUT =  [[VOID, PLAYER_2,   VOID,   PLAYER_2,   VOID,   PLAYER_2,   VOID,   PLAYER_2], 
                    [PLAYER_2, VOID,   PLAYER_2,   VOID,   PLAYER_2,   VOID,   PLAYER_2,   VOID], 
                    [VOID, PLAYER_2,    VOID,   PLAYER_2,  VOID, PLAYER_2,    VOID,    PLAYER_2], 
                    [VOID,     VOID,    VOID,       VOID,  VOID,     VOID,    VOID,        VOID],
                    [VOID,     VOID,    VOID,       VOID,  VOID,     VOID,    VOID,        VOID],
                    [PLAYER_1, VOID,   PLAYER_1,   VOID,   PLAYER_1,   VOID,   PLAYER_1,   VOID], 
                    [VOID, PLAYER_1,    VOID,   PLAYER_1,  VOID, PLAYER_1,    VOID,    PLAYER_1], 
                    [PLAYER_1, VOID,    PLAYER_1,   VOID,  PLAYER_1, VOID,    PLAYER_1,    VOID]]

class Board:
    def __init__(self, board: list, player1_left, player2_left):
        self.player1_left = player1_left
        self.player2_left = player2_left
        self.current_positions = board.copy()

    def make_moves(self, player, piece: tuple, moves: list):
        moves.reverse()
        for i in range(0, len(moves)):
            if i == 0:
                self.__make_move(player, piece, moves[i])
            else:
                self.__make_move(player, (moves[i - 1][1], moves[i - 1][2]), moves[i])

        return self.is_game_finished()

    def __make_move(self, player, piece: tuple, move: tuple):
        if move[0] == "capture":
            return self.__capture_piece(player, piece, (move[1], move[2]))
        else:
            return self.__move_near(player, piece, (move[1], move[2])) 

    # move to near void field
    def __move_near(self, player, piece: tuple, field: tuple):
        self.current_positions[piece[0]][piece[1]] = VOID
        self.current_positions[field[0]][field[1]] = player

        self.__change_to_king(player, field)

    def __change_to_king(self, player, field):
        if player == PLAYER_1 and field[0] == 0 or player == PLAYER_2 and field[0] == 7:
            self.current_positions[field[0]][field[1]] = PLAYER_1_KING if player == PLAYER_1 else PLAYER_2_KING

    # capture opponent's piece and move foward
    def __capture_piece(self, player, piece: tuple, field: tuple):
        # update remaining pieces
        if player == PLAYER_1 or player == PLAYER_1_KING:
            self.player2_left -= 1
        else:
            self.player1_left -= 1

        self.current_positions[piece[0]][piece[1]] = VOID
        self.current_positions[int((piece[0] + field[0]) / 2)][int((piece[1] + field[1]) / 2)] = VOID
        self.current_positions[field[0]][field[1]] = player

        self.__change_to_king(player, field)

    # check if game has ended and who is a winner
    def is_game_finished(self):
        if self.player1_left == 0:
            return PLAYER_2
        elif self.player2_left == 0:
            return PLAYER_1
        else:
            return 0

    # return all possible moves for active player
    def get_all_possible_moves(self, player):
        moves = []

        # create list with all possible moves for all active player's pieces 
        for i in range(0, 8):
            for j in range(0, 8):
                if self.current_positions[i][j] == player:
                    moves.extend(self.possible_moves_for_piece(player, (i, j)))
                elif self.__check_player(self.current_positions[i][j]) == self.__check_player(player):
                    moves.extend(self.possible_moves_for_piece(player + 2, (i, j)))

        capture_moves = self.__get_capture_moves(moves)

        # if there are some moves which are leading to capturing opponent's piece return only them
        if capture_moves != []:
            return capture_moves
        else:
            return moves

    def possible_moves_for_piece(self, player, piece: tuple):
        if player == PLAYER_1_KING or player == PLAYER_2_KING:
            return self.__king_moves(piece, player, -1)
        elif player == PLAYER_1:
            return self.__pawn_moves(piece, player, -1, None)
        else:
             return self.__pawn_moves(piece, player, 1, None)

    def __pawn_moves(self, piece, player, diff, previous_move):
        moves = []
        fields = self.__check_near_positions(player, piece, diff)

        for field in fields:
            # if this is first move and there is no piece on the field then this is possible move
            if field[0] == VOID and previous_move is None:
                moves.append([("near", field[1], field[2], piece[0], piece[1], player)])
            # if behind opponent's piece is void field then this is possible move
            elif self.__check_player(field[0]) != player and field[0] != VOID:
                field_column = field[2] + 1 if field[2] > piece[1] else field[2] - 1
                next_field = self.__check_position((field[1] + (field[1] - piece[0]) , field_column))

                if not next_field is None and next_field[0] == VOID:
                    if previous_move is None or next_field[1] != previous_move[0] or next_field[2] != previous_move[1]:
                        future_moves = self.__pawn_moves((next_field[1], next_field[2]), player, diff, piece)
                    
                        for m in future_moves:
                            m.append(("capture", next_field[1], next_field[2], piece[0], piece[1], player))
                    else:
                        future_moves = []

                    if future_moves != []:
                        moves.extend(future_moves)
                    elif previous_move is None:
                        moves.append([("capture", next_field[1], next_field[2], piece[0], piece[1], player)])
                    elif next_field[1] != previous_move[0] or next_field[2] != previous_move[1]:
                        moves.append([("capture", next_field[1], next_field[2], piece[0], piece[1], player)])

        return self.__filter_moves(moves)

    def __filter_moves(self, moves: list):
        # if there are some moves which are leading to capturing opponent's piece return only them
        capture_moves = self.__get_capture_moves(moves)
        if capture_moves != []:
            best_move = 0

            for move in capture_moves:
                if len(move) > best_move:
                    best_move = len(move)

            result = []
            for move in capture_moves:
                if len(move) == best_move:
                    result.append(move)

            return result
        else:
            return moves

    def __king_moves(self, piece, player, blocked_direction):
        fields = []
        moves = []

        # compute all possible fields
        if blocked_direction != 0:
            fields.append(self.__diagonal_fields(piece, player, -1, -1, lambda row: row >= 0, lambda column: column >= 0))
        if blocked_direction != 1:
            fields.append(self.__diagonal_fields(piece, player, 1, 1, lambda row: row <= 7, lambda column: column <= 7))
        if blocked_direction != 2:
            fields.append(self.__diagonal_fields(piece, player, 1, -1, lambda row: row <= 7, lambda column: column >= 0))
        if blocked_direction != 3:
            fields.append(self.__diagonal_fields(piece, player, -1, 1, lambda row: row >= 0, lambda column: column <= 7))

        for i in range(0, len(fields)):
            f = fields[i]
            last = len(f) - 1

            if f != []:
                if f[last][0] == VOID:
                    for field in f:
                        moves.append([("near", field[1], field[2], piece[0], piece[1], player)])
                elif self.__validate_field((f[last][1], f[last][2])) and self.current_positions[f[last][1]][f[last][2]] == VOID:
                    pass
                # calculate for every possible move again
                else:
                    for j in range(0, last):
                        moves.append([("near", f[j][1], f[j][2], piece[0], piece[1], player)])

        return moves

    # return all fields which might be king's move
    def __diagonal_fields(self, piece, player, row_diff, column_diff, row_cond, column_cond):
        fields = []
        row = piece[0]
        column = piece[1]

        while row_cond(row) and column_cond(column):
            row += row_diff
            column += column_diff

            if self.__validate_field((row, column)):
                if self.__check_player(self.current_positions[row][column]) == self.__check_player(player):
                    break
                elif self.current_positions[row][column] == VOID:
                    fields.append((self.current_positions[row][column], row, column))
                else:
                    fields.append((self.current_positions[row][column], row, column))
                    break

        return fields

    # check which moves are leading to capturing opponent's piece
    def __get_capture_moves(self, moves):
        capture_moves = []

        for move in moves:
            if move[0][0] == "capture":
                capture_moves.append(move)

        return capture_moves

    # check nearest 4 field of the piece
    def __check_near_positions(self, player, field, diff):
        fields = []

        f = self.__check_position((field[0] + diff, field[1] - 1))
        if not f is None:
            fields.append(f)

        f = self.__check_position((field[0] + diff, field[1] + 1))
        if not f is None:
            fields.append(f)

        # check if other player's piece is not on the back
        f = self.__check_position((field[0] - diff, field[1] - 1))
        if not f is None and self.__check_player(f[0]) != VOID and self.__check_player(f[0]) != player: 
            fields.append(f)

        f = self.__check_position((field[0] - diff, field[1] + 1))
        if not f is None and self.__check_player(f[0]) != VOID and self.__check_player(f[0]) != player: 
            fields.append(f)
        
        return fields
    
    # return type of the selected field
    def __check_position(self, field):
        if self.__validate_field(field):
            return (self.current_positions[field[0]][field[1]], *field)
    
    # check if selected field is on the board
    def __validate_field(self, field: tuple):
        if field[0] >= 0 and field[0] < 8 and field[1] >= 0 and field[1] < 8:
            return True
        else:
            return False
    
    # check which player it is
    def __check_player(self, player): 
        if player == PLAYER_1 or player == PLAYER_1_KING:
            return PLAYER_1
        elif player == VOID:
            return VOID
        else:
            return PLAYER_2
   