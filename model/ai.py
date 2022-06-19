import math
from model.board import Board
from copy import deepcopy

class Simple_AI:

	def __init__(self, depth):
		self.depth = depth

	def make_move(self, board: Board):
		copied_board = deepcopy(board)
		return self.__minimax(None, self.depth, -math.inf, math.inf, False, copied_board)[1]

	def __minimax(self, position, depth, alpha, beta, maximizing_player, board: Board):
		if depth == 0 or board.is_game_finished() == 1 or board.is_game_finished() == 2:
			return (board.player1_left - board.player2_left, position)

		if maximizing_player:
			max_eval = -math.inf
			best_move = None
			for move in board.get_all_possible_moves(self.__which_player(maximizing_player)):
				copied_board = deepcopy(board)
				copied_board.make_moves(self.__which_player(maximizing_player), (move[len(move) - 1][3], move[len(move) - 1][4]), move)

				eval = self.__minimax(move, depth - 1, alpha, beta, False, copied_board)[0]
				max_eval = max(max_eval, eval)

				best_move = move if max_eval == eval else best_move

				alpha = max(alpha, eval)
				if beta <= alpha:
					break

			return (max_eval, best_move)
		else:
			min_eval = math.inf
			best_move = None
			for move in board.get_all_possible_moves(self.__which_player(maximizing_player)):
				copied_board = deepcopy(board)
				copied_board.make_moves(self.__which_player(maximizing_player), (move[len(move) - 1][3], move[len(move) - 1][4]), move)

				eval = self.__minimax(move, depth - 1, alpha, beta, True, copied_board)[0]
				min_eval = min(min_eval, eval)

				best_move = move if min_eval == eval else best_move

				beta = min(beta, eval)
				if beta <= alpha:
					break

			return (min_eval, best_move)

	def __which_player(self, maximizing_player):
		if maximizing_player:
			return 1
		else:
			return 2