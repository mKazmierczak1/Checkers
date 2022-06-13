from tkinter import Frame
from model.board import Board
import view.windows as windows

# create instance of game board
board = Board()
turn = 1

# storage for all allowed moves which player can make
allowed_moves = board.get_all_possible_moves(turn)

# make move
def move(player, piece, field, frame: Frame):
    global allowed_moves

    # if game has finished draw proper element
    if board.make_move(player, piece, field):
        print("Game finished")
        windows.draw_winner_window(frame.master)

    # update turn
    next_turn()

    # update allowed moves
    allowed_moves = board.get_all_possible_moves(turn)

# return list of all moves for active player
def possible_moves(player, piece):
    print(allowed_moves)
    if player == turn:
        moves = board.possible_moves_for_piece(player, piece)
        result = []

        # check if possible moves for selected piece are allowed in this turn 
        for m in moves:
          if m in allowed_moves:
            result.append(m)

        return result  
    else:
        return []

# change turn
def next_turn():
    global turn
    turn = 1 if turn == 2 else 2