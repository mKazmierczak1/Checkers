from model.board import Board

board = Board()
turn = 1

def move(player, piece, field):
    board.move(player, piece, field)
    next_turn()

def possible_moves(player, piece):
    if player == turn:
        return board.possible_moves(player, piece)
    else:
        return []

def next_turn():
    global turn
    turn = 1 if turn == 2 else 2