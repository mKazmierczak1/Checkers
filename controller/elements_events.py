from tkinter import *
from constans import *
import view.elements as elements
import view.frames as frames
from controller.game_controller import Game_controller

highlighted_fields = []
game: Game_controller = None

# bind highlighting possible moves function with piece
def bind_func_with_piece(canvas, row, column, frame: Frame, color):
    func = lambda event: highlight_possible_moves(check_player(color), (row, column), frame, event)
    canvas.bind('<Button-1>', func)

def check_player(color):
    if color == RED:
        return 1
    elif color == PURPLE:
        return 2
    elif color == ORANGE:
        return 3
    else:
        return 4

# highlight fields on which you can move piece
def highlight_possible_moves(player, piece: tuple, frame: Frame, event):
    global highlighted_fields
    
    # remove old highlighted fields
    for hf in highlighted_fields:
        elements.draw_field(hf[1], hf[2], frame, BLACK)

    # create new highlighted fields
    highlighted_fields = game.possible_moves(player, piece)
    for hf in highlighted_fields:
        canvas = elements.draw_field(hf[1], hf[2], frame, LIGHT_BLUE)
        bind_move_func(canvas, hf[5], piece, hf, frame)

# bind function for moving piece with highlighted field
def bind_move_func(canvas, player, piece: tuple, move: tuple, frame: Frame):
    func = lambda event: move_piece(player, piece, move, frame, event)
    canvas.bind('<Button-1>', func)

# move piece to highlighted field and update view after changes on the board
def move_piece(player, piece: tuple, move: tuple, frame: Frame, event):
    global highlighted_fields

    # remove old highlighted fields
    for hf in highlighted_fields:
        elements.draw_field(hf[1], hf[2], frame, BLACK)

    highlighted_fields.clear()

    # make move on the board
    if not game.move(player, piece, move, frame):
        # update view after changes on the board
        window = frame.master
        clean_window(window)
        frames.draw_all_pieces(frames.get_board_frame(window))

# remove all elements present on the window
def clean_window(window: Tk):
    for widget in window.winfo_children():
        widget.destroy()