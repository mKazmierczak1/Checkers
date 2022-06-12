from board import PLAYER_1
class Piece:
    def __init__(self, player):
        self.player = player
        self.is_king = False

        if player == PLAYER_1:
            self.directions = -1
        else:
            self.directions = 1