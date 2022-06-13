VOID = 0
PLAYER_1 = 1
PLAYER_2 = 2
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

    def move(self, player, piece: tuple, move: tuple):
        if not self.__validate_piece:
            raise Exception("Wrong piece!")

        if move[0] == "capture":
            self.__capture_piece()
        else:
            self.__move_near(player, piece, (move[1], move[2]))

        

    def __move_near(self, player, piece: tuple, field: tuple):
        self.current_positions[piece[0]][piece[1]] = VOID
        self.current_positions[field[0]][field[1]] = player

    def __capture_piece(self, player, piece: tuple, field: tuple):
        if player == PLAYER_1:
            self.player2_left -= 1
        else:
            self.player1_left -= 1

        self.current_positions[piece[0]][piece[1]] = VOID
        self.current_positions[(piece[0] + field[0]) / 2][(piece[1] + field[1]) / 2] = VOID
        self.current_positions[field[0]][field[1]] = player

    def possible_moves(self, player, piece: tuple):
        if not self.__validate_piece:
            raise Exception("Wrong piece!")

        moves = []

        if player == PLAYER_1:
            diff = -1
        else:
            diff = 1

        near = self.__check_near_positions(piece, diff)
        
        for n in near:
            print(near)
            if not n is None and n[0] != VOID and n[0] != player:
                field_column = n[2] + 1 if n[2] > piece[1] else n[2] - 1
                next_field = self.__check_position((n[1] + diff, field_column))

                if next_field[0] == VOID:
                    moves.append(("capture", next_field[1], next_field[2]))
        
        if moves != []:
            return moves

        for n in near:
            if not n is None and n[0] == VOID:
                moves.append(("near", n[1], n[2]))

        return moves


    def __check_near_positions(self, field, diff):
        fields = []

        fields.append(self.__check_position((field[0] + diff, field[1] - 1)))
        fields.append(self.__check_position((field[0] + diff, field[1] + 1)))
        
        return fields
    
    def __check_position(self, field):
        if self.__validate_field(field):
            return (self.current_positions[field[0]][field[1]], field[0], field[1])

    def __validate_player(self, player):
        if player == 1 or player == 2:
            return True
        else:
            return False
    
    def __validate_field(self, field: tuple):
        if field[0] >= 0 and field[0] < 8 and field[1] >= 0 and field[1] < 8:
            return True
        else:
            return False
    
    def __validate_piece(self, player, piece: tuple):
        if not self.__validate_player(player):
            raise Exception("Wrong player number!")

        if not self.__validate_field(piece):
            raise Exception("Wrong field number!")

        if self.current_positions[piece[0]][piece[1]] == player:
            return True
        else:
            return False