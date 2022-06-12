from tkinter import *
from model.board import *
from constans import *

board = Board()
highlighted_fields = []

def get_window():
    window = Tk()
    window.title("Chekers")
    window.geometry(str(WIDTH) + "x" + str(HEIGHT))
    window.resizable(False, False)

    return window

def get_main_menu_window():
    window = get_window()
    get_board_frame(window)
    
    label = Label(window, text="CHECKERS", font=("Comic Sans MS", 56), background=RED, bd=4, relief="groove")
    label.place(x = 155, y = 20)

    buttons_frame = Frame(window, background=RED, height=300, width=300, bd=4, relief="groove")
    buttons_frame.place(x=200, y=300)

    single_player_button = Button(buttons_frame, text="Singleplayer", font=("Comic Sans MS", 24), foreground=WHITE, background=PURPLE, 
                                    command=get_starting_board_frame, bd=4, relief="groove").place(x = 40, y = 40)
    multi_player_button = Button(buttons_frame, text="Multiplayer ", font=("Comic Sans MS", 24), foreground=WHITE, background=PURPLE, 
                                    command=get_starting_board_frame, bd=4, relief="groove").place(x = 40, y = 170)

    return window

def get_board_frame(master_window):
    board_frame = Frame(master_window)
    board_frame.pack()

    for i in range(0, 8):
        for j in range(0, 8):
            canvas = Canvas(board_frame, width=WIDTH/8 - WIDTH/85, height=HEIGHT/8 - HEIGHT/85)
            draw_field(i, j, board_frame, WHITE if (i + j) % 2 == 0 else BLACK)
            canvas.grid(row=i, column=j, padx=2, pady=2)

def get_empty_board_window():
    window = get_window()
    get_board_frame(window)

    return window

def get_starting_board_frame():
    window = get_window()
    get_board_frame(window)
    draw_all_pieces(window.children["!frame"])

    return window

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
    func = lambda event: highlight_possible_moves(1 if color == RED else 2, (row, column), frame, event)
    canvas.bind('<Button-1>', func)

def highlight_possible_moves(player, piece: tuple, frame: Frame, event):
    global highlighted_fields
    
    for hf in highlighted_fields:
        draw_field(*hf, frame, BLACK)

    highlighted_fields = board.possible_moves(player, piece)

    for hf in highlighted_fields:
        canvas = draw_field(*hf, frame, LIGHT_BLUE)
        bind_move_func(canvas, player, piece, hf, frame)


def bind_move_func(canvas, player, piece: tuple, field: tuple, frame: Frame):
    func = lambda event: move_piece(player, piece, field, frame, event)
    canvas.bind('<Button-1>', func)

def move_piece(player, piece: tuple, field: tuple, frame: Frame, event):
    global highlighted_fields

    for hf in highlighted_fields:
        draw_field(*hf, frame, BLACK)

    highlighted_fields.clear()

    draw_field(*piece, frame, BLACK)
    draw_piece(*field, frame, RED if player == 1 else PURPLE)

    board.move(player, piece, field)

def draw_all_pieces(frame:Frame):
    for i in range(0, 8):
        for j in range(0, 8):
            if CHECKERS_LAYOUT[i][j] == PLAYER_1:
                draw_piece(i, j, frame, RED)
            elif CHECKERS_LAYOUT[i][j] == PLAYER_2:
                draw_piece(i, j, frame, PURPLE)