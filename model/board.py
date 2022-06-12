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

    def move(self, player, piece: tuple, field: tuple):
        if not self.__validate_piece:
            raise Exception("Wrong piece!")

        self.current_positions[piece[0]][piece[1]] = VOID
        self.current_positions[field[0]][field[1]] = player


    def possible_moves(self, player, piece: tuple):
        if not self.__validate_piece:
            raise Exception("Wrong piece!")

        moves = []

        if player == PLAYER_1:
            diff = -1
        else:
            diff = 1

        move = (piece[0] + diff, piece[1] - 1)

        if self.__validate_field(move) and self.current_positions[move[0]][move[1]] == VOID:
            moves.append((move))

        move = (piece[0] + diff, piece[1] + 1)

        if self.__validate_field(move) and self.current_positions[move[0]][move[1]] == VOID:
            moves.append((move))

        return moves


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