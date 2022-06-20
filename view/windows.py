from tkinter import *
from constans import *
from model.ai import Simple_AI
import view.frames as frames
import controller.elements_events as elem_events
from controller.game_controller import Game_controller

# return template window
def get_window():
    window = Tk()
    window.title("Chekers")
    window.geometry(str(WIDTH) + "x" + str(HEIGHT))
    window.resizable(False, False)

    return window

# create main menu window
def get_main_menu_window():
    window = get_window()
    frames.get_board_frame(window)
    
    label = Label(window, text="CHECKERS", font=("Comic Sans MS", 56), background=RED, bd=4, relief="groove")
    label.place(x = 155, y = 20)

    buttons_frame = Frame(window, background=RED, height=300, width=300, bd=4, relief="groove")
    buttons_frame.place(x=200, y=300)

    single_player_button = Button(buttons_frame, text="Singleplayer", font=("Comic Sans MS", 24), foreground=WHITE, background=PURPLE, 
                                    command=lambda: draw_level_choice_window(window), bd=4, relief="groove").place(x = 40, y = 40)
    
    multi_player_button = Button(buttons_frame, text="Multiplayer ", font=("Comic Sans MS", 24), foreground=WHITE, background=PURPLE, 
                                    command=lambda: get_starting_board_widow(False, 0), bd=4, relief="groove").place(x = 40, y = 170)

    return window

# return simple checked game board without pieces on it
def get_empty_board_window():
    window = get_window()
    frames.get_board_frame(window)

    return window

# return window with game board with pieces on their starting positions
def get_starting_board_widow(singleplayer, ai_level):
    window = get_window()

    if singleplayer:
        elem_events.game = Game_controller(Simple_AI(ai_level), window)
    else:
        elem_events.game = Game_controller(None, window)

    frames.get_board_frame(window)
    frames.draw_all_pieces(window.children["!frame"])

    return window

# create window for user to choose ai difficulty
def draw_level_choice_window(window: Tk):
    winner_frame = Frame(window, background=RED, height=300, width=300, bd=4, relief="groove")
    easy_button = Button(winner_frame, text="  Easy  ", font=("Comic Sans MS", 24), foreground=WHITE, background=PURPLE, 
                                    command=lambda: choose_level(window, 1), bd=4, relief="groove").place(x = 70, y = 5)
    medium_button = Button(winner_frame, text="Medium", font=("Comic Sans MS", 24), foreground=WHITE, background=PURPLE, 
                                    command=lambda: choose_level(window, 3), bd=4, relief="groove").place(x = 70, y = 100)
    hard_button = Button(winner_frame, text="  Hard  ", font=("Comic Sans MS", 24), foreground=WHITE, background=PURPLE, 
                                    command=lambda: choose_level(window, 5), bd=4, relief="groove").place(x = 70, y = 200)
                                    
    winner_frame.place(x = 200, y = 300)

# change ai level and destory choose level frame
def choose_level(window: Tk, level):
    childern = list(window.children.keys())
    window.children[childern[len(childern) - 1]].destroy()

    get_starting_board_widow(True, level)
    

# when game has finished draw a info with the result of the game
def draw_winner_window(window: Tk, player):
    winner_frame = Frame(window, background=RED, height=300, width=300, bd=4, relief="groove")
    label = Label(winner_frame, text="Player " + str(player) + " won!", font=("Comic Sans MS", 32), background=RED).place(x = 12, y = 30)
    exit_button = Button(winner_frame, text="Exit", font=("Comic Sans MS", 24), foreground=WHITE, background=PURPLE, 
                                    command=lambda: exit(window), bd=4, relief="groove").place(x = 100, y = 150)

    winner_frame.place(x = 200, y = 300)

def exit(window):
    window.destroy()