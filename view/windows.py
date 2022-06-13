from tkinter import *
from constans import *
import view.frames as frames

def get_window():
    window = Tk()
    window.title("Chekers")
    window.geometry(str(WIDTH) + "x" + str(HEIGHT))
    window.resizable(False, False)

    return window

def get_main_menu_window():
    window = get_window()
    frames.get_board_frame(window)
    
    label = Label(window, text="CHECKERS", font=("Comic Sans MS", 56), background=RED, bd=4, relief="groove")
    label.place(x = 155, y = 20)

    buttons_frame = Frame(window, background=RED, height=300, width=300, bd=4, relief="groove")
    buttons_frame.place(x=200, y=300)

    single_player_button = Button(buttons_frame, text="Singleplayer", font=("Comic Sans MS", 24), foreground=WHITE, background=PURPLE, 
                                    command=get_starting_board_widow, bd=4, relief="groove").place(x = 40, y = 40)
    multi_player_button = Button(buttons_frame, text="Multiplayer ", font=("Comic Sans MS", 24), foreground=WHITE, background=PURPLE, 
                                    command=get_starting_board_widow, bd=4, relief="groove").place(x = 40, y = 170)

    return window

def get_empty_board_window():
    window = get_window()
    frames.get_board_frame(window)

    return window

def get_starting_board_widow():
    window = get_window()
    frames.get_board_frame(window)
    frames.draw_all_pieces(window.children["!frame"])

    return window