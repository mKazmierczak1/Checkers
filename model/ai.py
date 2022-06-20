import math
from model.board import Board
from copy import deepcopy

class Simple_AI:

	def __init__(self, depth):
		self.depth = depth

	# return move which was calculated with minimax algorithm
	def make_move(self, board: Board):
		copied_board = deepcopy(board)
		return self.__minimax(None, self.depth, -math.inf, math.inf, False, copied_board)[1]

	# implementation of minimax algorithm with alpha beta pruning
	# short explanation: simulation of few moves ahead (number of moves depends from depth and it also means how difficult ai is)
	# in the simulation every player is trying to make as the best move as it is possible
	# so the goal is to choose a path that is the most likely to happen and where the result is also the best
	# alpha beta pruning is a method which hepls to estimate if some path is worth exploring or can be already skipped
	def __minimax(self, position, depth, alpha, beta, maximizing_player, board: Board):
		if depth == 0 or board.is_game_finished() == 1 or board.is_game_finished() == 2:
			return (board.player1_left - board.player2_left, position)

		if maximizing_player:
			max_eval = -math.inf
			best_move = None
			for move in board.get_all_possible_moves(self.__which_player(maximizing_player)):
				copied_board = deepcopy(board)
				copied_board.make_moves(move[len(move) - 1][5], (move[len(move) - 1][3], move[len(move) - 1][4]), move)

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
				copied_board.make_moves(move[len(move) - 1][5], (move[len(move) - 1][3], move[len(move) - 1][4]), move)

				eval = self.__minimax(move, depth - 1, alpha, beta, True, copied_board)[0]
				min_eval = min(min_eval, eval)

				best_move = move if min_eval == eval else best_move

				beta = min(beta, eval)
				if beta <= alpha:
					break

			return (min_eval, best_move)

	# check which player is currently making his move in a simulation
	def __which_player(self, maximizing_player):
		if maximizing_player:
			return 1
		else:
			return 2