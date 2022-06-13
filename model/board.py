# constants which are specifying what is on a field on the game board
VOID = 0
PLAYER_1 = 1
PLAYER_2 = 2

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
    def __init__(self):
        self.player1_left = 12
        self.player2_left = 12
        self.current_positions = CHECKERS_LAYOUT.copy()

    def make_move(self, player, piece: tuple, move: tuple):
        if not self.__validate_piece:
            raise Exception("Wrong piece!")

        print(move)
        if move[0] == "capture":
            return self.__capture_piece(player, piece, (move[1], move[2]))
        else:
            return self.__move_near(player, piece, (move[1], move[2])) 

    # move to near void field
    def __move_near(self, player, piece: tuple, field: tuple):
        self.current_positions[piece[0]][piece[1]] = VOID
        self.current_positions[field[0]][field[1]] = player

        return 0

    # capture opponent's piece and move foward
    def __capture_piece(self, player, piece: tuple, field: tuple):
        # update remaining pieces
        if player == PLAYER_1:
            self.player2_left -= 1
        else:
            self.player1_left -= 1

        self.current_positions[piece[0]][piece[1]] = VOID
        self.current_positions[int((piece[0] + field[0]) / 2)][int((piece[1] + field[1]) / 2)] = VOID
        self.current_positions[field[0]][field[1]] = player

        return self.is_game_finished()

    # check if game has ended and who is a winner
    def is_game_finished(self):
        if self.player1_left == 0:
            return PLAYER_2
        elif self.player2_left == 0:
            return PLAYER_1
        else:
            return 0

    def possible_moves_for_piece(self, player, piece: tuple):
        if not self.__validate_piece:
            raise Exception("Wrong piece!")

        moves = []

        if player == PLAYER_1:
            diff = -1
        else:
            diff = 1

        near = self.__check_near_positions(player, piece, diff)
        
        for n in near:
            if not n is None and n[0] != VOID and n[0] != player:
                field_column = n[2] + 1 if n[2] > piece[1] else n[2] - 1
                next_field = self.__check_position((n[1] + diff, field_column))

                if not next_field is None and next_field[0] == VOID and (diff > 0 and n[1] > piece[0] or diff < 0 and n[1] < piece[0]):
                    moves.append(("capture", next_field[1], next_field[2]))
                
                if diff > 0 and n[1] < piece[0] or diff < 0 and n[1] > piece[0]:
                    back_field = self.__check_position((n[1] - diff, field_column))
                    if  not back_field is None and back_field[0] == VOID:
                        moves.append(("capture", back_field[1], back_field[2]))
                
        if moves != []:
            return moves

        for n in near:
            if not n is None and n[0] == VOID:
                moves.append(("near", n[1], n[2]))

        return moves

    # return all possible moves for active player
    def get_all_possible_moves(self, player):
        moves = []

        # create list with all possible moves for all active player's pieces 
        for i in range(0, 8):
            for j in range(0, 8):
                if self.current_positions[i][j] == player:
                    moves.extend(self.possible_moves_for_piece(player, (i, j)))

        capture_moves = self.__get_capture_moves(moves)

        # if there are some moves which are leading to capturing opponent's piece return only them
        if capture_moves != []:
            return capture_moves
        else:
            return moves

    # check which moves are leading to capturing opponent's piece
    def __get_capture_moves(self, moves):
        capture_moves = []

        for move in moves:
            if move[0] == "capture":
                capture_moves.append(move)

        return capture_moves

    # check nearest 4 field of the piece
    def __check_near_positions(self, player, field, diff):
        fields = []

        fields.append(self.__check_position((field[0] + diff, field[1] - 1)))
        fields.append(self.__check_position((field[0] + diff, field[1] + 1)))

        # check if other player's piece is not on the back
        back = self.__check_position((field[0] - diff, field[1] - 1))
        if not back is None and back[0] != VOID and back != player: 
            fields.append(back)

        back = self.__check_position((field[0] - diff, field[1] + 1))
        if not back is None and back[0] != VOID and back != player: 
            fields.append(back)
        
        return fields
    
    # return type of the selected field
    def __check_position(self, field):
        if self.__validate_field(field):
            return (self.current_positions[field[0]][field[1]], field[0], field[1])

    # check if player was selected correctly
    def __validate_player(self, player):
        if player == 1 or player == 2:
            return True
        else:
            return False
    
    # check if selected field is on the board
    def __validate_field(self, field: tuple):
        if field[0] >= 0 and field[0] < 8 and field[1] >= 0 and field[1] < 8:
            return True
        else:
            return False
    
    # check if player selected his own piece
    def __validate_piece(self, player, piece: tuple):
        if not self.__validate_player(player):
            raise Exception("Wrong player number!")

        if not self.__validate_field(piece):
            raise Exception("Wrong field number!")

        if self.current_positions[piece[0]][piece[1]] == player:
            return True
        else:
            return False