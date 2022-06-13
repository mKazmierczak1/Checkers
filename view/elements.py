from tkinter import *
from constans import *
import controller.elements_events as elem_events

# create simple square with specified color on given position 
def draw_field(row, column, frame: Frame, color):
    # compute field number
    number = row * 8 + column + 1
    nr = "" if number == 1 else str(number)

    # remove old elements and create new one
    canvas = frame.children["!canvas" + str(nr)]
    canvas.delete("all")
    canvas.unbind('<Button-1>')

    canvas.create_rectangle(2, 2, 100, 100, fill=color)

    return canvas

# create simple circle with specified color on given position and bind event handling to it
def draw_piece(row, column, frame: Frame, color):
    # compute field number
    number = row * 8 + column + 1
    nr = "" if number == 1 else str(number)

    # create new piece
    canvas = frame.children["!canvas" + str(nr)]
    canvas.create_oval(15, 15, 70, 70, fill=color)

    # bind event handling to the piece
    func = lambda event: elem_events.highlight_possible_moves(1 if color == RED else 2, (row, column), frame, event)
    canvas.bind('<Button-1>', func)

