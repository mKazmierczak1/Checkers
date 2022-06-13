from tkinter import *
from model.board import *
from constans import *
import view.elements as elements
import controller.game_controller as game

# return empty checked board
def get_board_frame(master_window):
    board_frame = Frame(master_window)
    board_frame.pack()

    # create checked game board
    # size is 8 squares x 8 squares
    for i in range(0, 8):
        for j in range(0, 8):
            canvas = Canvas(board_frame, width=WIDTH/8 - WIDTH/85, height=HEIGHT/8 - HEIGHT/85)
            elements.draw_field(i, j, board_frame, WHITE if (i + j) % 2 == 0 else BLACK)
            canvas.grid(row=i, column=j, padx=2, pady=2)
    
    return board_frame

# draw all pieces on their current positions
def draw_all_pieces(frame:Frame):
    for i in range(0, 8):
        for j in range(0, 8):
            if game.board.current_positions[i][j] == PLAYER_1:
                elements.draw_piece(i, j, frame, RED)
            elif game.board.current_positions[i][j] == PLAYER_2:
                elements.draw_piece(i, j, frame, PURPLE)
