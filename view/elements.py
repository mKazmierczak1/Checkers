from tkinter import *
from constans import *
import controller.elements_events as elem_events

def draw_field(row, column, frame: Frame, color):
    number = row * 8 + column + 1
    nr = "" if number == 1 else str(number)

    canvas = frame.children["!canvas" + str(nr)]
    canvas.delete("all")
    canvas.unbind('<Button-1>')

    canvas.create_rectangle(2, 2, 100, 100, fill=color)

    return canvas

def draw_piece(row, column, frame: Frame, color):
    number = row * 8 + column + 1
    nr = "" if number == 1 else str(number)
    canvas = frame.children["!canvas" + str(nr)]
    canvas.create_oval(15, 15, 70, 70, fill=color)
    func = lambda event: elem_events.highlight_possible_moves(1 if color == RED else 2, (row, column), frame, event)
    canvas.bind('<Button-1>', func)

