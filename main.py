import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, ROWS, COLS, BLACK_PIECES, WHITE_PIECES
from checkers.board import Board
from checkers.game import Game
from AI import minmax
import time
from AI import alphabeta
from checkers.piece import Piece

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Checkers")


def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


def main(player1AI, player2AI, depth, showAISearching, white_player_number, black_player_number):

    file = open('moves.txt', "w")

    start_time = time.time()
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    AIWIN = WIN if showAISearching else None

    # game.board.board = []
    # for i in range(8):
    #     game.board.board.append([0,0,0,0,0,0,0,0])
    # game.board.board[7][4] = Piece(7, 4, BLACK_PIECES)
    # game.board.board[7][4].make_king()
    # game.board.board[1][2] = Piece(1,2,WHITE_PIECES)
    # game.board.board[2][3] = Piece(2,3,WHITE_PIECES)
    # game.board.board[3][4] = Piece(3,4,WHITE_PIECES)
    # game.board.board[4][5]= Piece(4,5,WHITE_PIECES)
    # game.board.board[5][6]= Piece(5,6,WHITE_PIECES)
    # game.board.board[6][1]= Piece(6,1,WHITE_PIECES)
    # game.board.board[5][2]= Piece(5,2,WHITE_PIECES)
    # game.board.board[4][3]= Piece(4,3,WHITE_PIECES)
    # game.board.board[2][5]= Piece(2,5,WHITE_PIECES)
    # game.board.board[1][6]= Piece(1,6,WHITE_PIECES)


    # game.change_turn()
    game.board.calculate_all_moves(game.turn)

    while run:
        clock.tick(FPS)
        game.update()

        if game.turn == WHITE_PIECES:
            if player1AI:
                # value, move, row, col = minmax.minmax(game, depth, True, AIWIN, white_player_number)
                value, move, row, col = alphabeta.alphabeta(game, depth, True, float('-inf'), float('+inf'), AIWIN, white_player_number)
                file.write(f'{move[0]}, {move[1]} --> {row}, {col}\n')
                game.select(row, col)
                game.select(move[0], move[1])

        else:
            if player2AI:
                # value, move, row, col = minmax.minmax(game, depth, False, AIWIN, black_player_number)
                value, move, row, col = alphabeta.alphabeta(game, depth, False, float('-inf'), float('+inf'), AIWIN, black_player_number)
                file.write(f'{move[0]}, {move[1]} --> {row}, {col}\n')
                game.select(row, col)
                game.select(move[0], move[1])


        if game.board.winner(game.turn) != None:
            print(game.board.winner(game.turn))
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)



    pygame.quit()
    print(time.time() - start_time)


main(False, True, 3, False, 1, 1)