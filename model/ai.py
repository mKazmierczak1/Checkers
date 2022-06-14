import math
import controller.game_controller as game
from model.board import Board


def make_move():
	possible_moves = game.allowed_moves
	board = Board(game.board.current_positions, game.board.player1_left, game.board.player2_left)

	minimax(possible_moves, 3, -math.inf, math.inf, True)

def minimax(position, depth, alpha, beta, maximizingPlayer, board: Board):
	if depth == 0 or board.is_game_finished() == 1 or board.is_game_finished() == 2 in position:
		return board.player1_left - board.player2_left
 
	if maximizingPlayer:
		maxEval = -math.inf
		for child in position:
			eval = minimax(child, depth - 1, alpha, beta, False)
			maxEval = max(maxEval, eval)
			alpha = max(alpha, eval)
			if beta <= alpha:
				break
		return maxEval
 
	else:
		minEval = math.inf
		for child in position:
			eval = minimax(child, depth - 1, alpha, beta, True)
			minEval = min(minEval, eval)
			beta = min(beta, eval)
			if beta <= alpha:
				break
		return minEval

# minimax(currentPosition, 3, -math.inf, math.inf, True)