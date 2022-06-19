from tkinter import Frame, Tk
from model.board import Board, CHECKERS_LAYOUT
from model.ai import Simple_AI
import view.windows as windows
import view.frames as frames
from copy import deepcopy

class Game_controller:

    # create instance of game board
    def __init__(self, ai: Simple_AI, window: Tk):
        self.board = Board(deepcopy(CHECKERS_LAYOUT), 12, 12)
        self.ai = ai
        self.turn = 1
        self.window = window

        # storage for all allowed moves which player can make
        self.allowed_moves = self.board.get_all_possible_moves(self.turn)

    # make move
    def move(self, player, piece, field, frame: Frame):
        moves = [field]

        for m in self.allowed_moves:
            if m[0][1] == field[1] and m[0][2] == field[2]:
                moves = m

        # if game has finished draw proper element
        if self.board.make_moves(player, piece, moves):
            print("Game finished")
            windows.draw_winner_window(self.window, player)
        else:
            # update turn
            self.__next_turn()

            # update allowed moves
            self.allowed_moves = self.board.get_all_possible_moves(self.turn)

    # return list of all moves for active player
    def possible_moves(self, player, piece):
        if player == self.turn or player == (self.turn + 2):
            
            moves = self.board.possible_moves_for_piece(player, piece)
            result = []

            # check if possible moves for selected piece are allowed in this turn 
            for m in moves:
                if m in self.allowed_moves:
                    result.append(m[0])

            return result  
        else:
            return []

    # change turn
    def __next_turn(self):
        if self.ai is None:
            self.turn = 1 if self.turn == 2 else 2
        else:
            ai_move = self.ai.make_move(self.board)
            self.board.make_moves(2, (ai_move[0][3], ai_move[0][4]), ai_move)
            self.__update_window()

    def __update_window(self):
        for widget in self.window.winfo_children():
            widget.destroy()

        frames.draw_all_pieces(frames.get_board_frame(self.window))
    