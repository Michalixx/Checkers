import copy
from checkers.board import Board
from checkers.game import Game
from checkers.constants import WHITE_PIECES, BLACK_PIECES


def alphabeta(game, depth, maximizingPlayer, alpha, beta, WIN, player_number):
    if game.board.winner(game.turn) == WHITE_PIECES:
        return float('inf'), (-1, -1), -1, -1
    elif game.board.winner(game.turn) == BLACK_PIECES:
        return float('-inf'), (-1, -1), -1, -1
    elif game.board.winner(game.turn) == "REMIS":
        return 0, (-1, -1), -1, -1
    elif depth == 0:
        return game.board.evaluate(player_number), (-1, -1), -1, -1
    if maximizingPlayer:
        maxEval = float('-inf')
        best_move = None
        best_piece = None
        game.board.calculate_all_moves(game.turn)
        all_moves = game.board.possible_moves
        for piece in all_moves:
            for move in all_moves[piece]:
                game_copy = Game(WIN)
                game_copy.board = copy.deepcopy(game.board)
                game_copy.board.board = copy.deepcopy(game.board.board)
                game_copy.turn = game.turn
                game_copy.board.calculate_all_moves(game_copy.turn)
                game_copy.selected = False
                game_copy.select(piece.row, piece.col)
                game_copy.select(move[0], move[1])
                game_copy.update()
                evaluation = alphabeta(game_copy, depth-1, False, alpha, beta, WIN, player_number)[0]
                maxEval = max(maxEval, evaluation)
                alpha = max(alpha, evaluation)
                if maxEval == evaluation:
                    best_move = move
                    best_piece = piece
                if beta <= alpha:
                    return maxEval, best_move, best_piece.row, best_piece.col
        return maxEval, best_move, best_piece.row, best_piece.col
    else:
        minEval = float('inf')
        best_move = None
        best_piece = None
        game.board.calculate_all_moves(game.turn)
        all_moves = game.board.possible_moves
        for piece in all_moves:
            for move in all_moves[piece]:
                game_copy = Game(WIN)
                game_copy.board = copy.deepcopy(game.board)
                game_copy.board.board = copy.deepcopy(game.board.board)
                game_copy.turn = game.turn
                game_copy.board.calculate_all_moves(game_copy.turn)
                game_copy.selected = False
                game_copy.select(piece.row, piece.col)
                game_copy.select(move[0], move[1])
                game_copy.update()
                evaluation = alphabeta(game_copy, depth - 1, False, alpha, beta, WIN, player_number)[0]
                minEval = min(minEval, evaluation)
                beta = min(beta, evaluation)

                if minEval == evaluation:
                    best_move = move
                    best_piece = piece
                if beta <= alpha:
                    return minEval, best_move, best_piece.row, best_piece.col

        if best_piece == None:
            return minEval, best_move, -1, -1
        return minEval, best_move, best_piece.row, best_piece.col