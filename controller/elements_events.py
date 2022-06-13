from tkinter import *
from constans import *
import view.elements as elements
import controller.single_game_controller as game

highlighted_fields = []

def bind_func_with_piece(canvas, row, column, frame: Frame, color):
    func = lambda event: highlight_possible_moves(1 if color == RED else 2, (row, column), frame, event)
    canvas.bind('<Button-1>', func)

def highlight_possible_moves(player, piece: tuple, frame: Frame, event):
    global highlighted_fields
    
    for hf in highlighted_fields:
        elements.draw_field(hf[1], hf[2], frame, BLACK)

    highlighted_fields = game.possible_moves(player, piece)

    for hf in highlighted_fields:
        canvas = elements.draw_field(hf[1], hf[2], frame, LIGHT_BLUE)
        bind_move_func(canvas, player, piece, (hf[1], hf[2]), frame)

def highlight_possible_moves(player, piece: tuple, frame: Frame, event):
    global highlighted_fields
    
    for hf in highlighted_fields:
        elements.draw_field(hf[1], hf[2], frame, BLACK)

    highlighted_fields = game.possible_moves(player, piece)

    for hf in highlighted_fields:
        canvas = elements.draw_field(hf[1], hf[2], frame, LIGHT_BLUE)
        bind_move_func(canvas, player, piece, (hf[1], hf[2]), frame)

def bind_move_func(canvas, player, piece: tuple, field: tuple, frame: Frame):
    func = lambda event: move_piece(player, piece, field, frame, event)
    canvas.bind('<Button-1>', func)

def move_piece(player, piece: tuple, field: tuple, frame: Frame, event):
    global highlighted_fields

    for hf in highlighted_fields:
        elements.draw_field(hf[1], hf[2], frame, BLACK)

    highlighted_fields.clear()

    elements.draw_field(*piece, frame, BLACK)
    elements.draw_piece(*field, frame, RED if player == 1 else PURPLE)

    game.move(player, piece, field)