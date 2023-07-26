import random

import pygame
from .constants import BLACK_SQUARES, ROWS, WHITE_PIECES, SQUARE_SIZE, COLS, BLACK_PIECES, LIGHT_SQUARES
from .piece import Piece

class Board:

    def __init__(self):
        self.board = []
        self.white_left = self.black_left = 12
        self.white_kings = self.black_kings = 0
        self.create_board()
        self.possible_moves = {}
        self.moves_without_take = 0
        self.king_moves_in_a_row = 0

    # Draws a chessboard
    # @Param {win} pygame window
    def draw_squares(self, win):
        if win is None:
            return
        win.fill(BLACK_SQUARES)
        for row in range(ROWS):
            for col in range(row % 2, ROWS, 2):
                pygame.draw.rect(win, LIGHT_SQUARES, (row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row+1)%2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, BLACK_PIECES))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, WHITE_PIECES))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)
        if piece.king:
            self.king_moves_in_a_row += 1
        else:
            self.king_moves_in_a_row = 0

        if piece.color == BLACK_PIECES and row == ROWS - 1:
            piece.make_king()
            self.black_kings += 1
        if piece.color == WHITE_PIECES and row == 0:
            piece.make_king()
            self.white_kings += 1

    def get_piece(self, row, col):
        if row >=  ROWS or row < 0:
            return -1
        if col >= COLS or col < 0:
            return -1
        return self.board[row][col]

    def get_valid_moves2(self, piece):
        moves = {}

        if piece.king:
            moves.update(self._king_normal_moves(piece))
            moves.update(self._king_takes(piece.row, piece.col, piece.color, []))
        else:
            moves.update(self._more_jumps_check(piece.row, piece.col, piece.color, []))
            left = piece.col - 1
            right = piece.col + 1
            row = piece.row
            row_modifier = -1 if piece.color == WHITE_PIECES else 1

            if left >= 0 and self.get_piece(row+row_modifier, left) == 0 and row+row_modifier >= 0 and row+row_modifier < ROWS:
                moves[(row+row_modifier, left)] = []

            if right <= COLS and self.get_piece(row+row_modifier, right) == 0 and row+row_modifier >= 0 and row+row_modifier < ROWS:
                moves[(row+row_modifier, right)] = []

        # max_takes = 0
        # moves_with_takes_rule = {}
        # for move in moves:
        #     if max_takes < len(moves[move]):
        #         max_takes = len(moves[move])
        # for move in moves:
        #     if max_takes == len(moves[move]):
        #         moves_with_takes_rule[move] = moves[move]
        #
        # return moves_with_takes_rule
        return moves


    def _more_jumps_check(self, row, col, color, jumped):
        moves = {}
        for i in [-1, 1]:
            for j in [-1, 1]:
                first_piece = self.get_piece(row + i, col + j)
                if first_piece != 0 and first_piece != -1 and first_piece.color != color and first_piece not in jumped:
                    if self.get_piece(row + 2*i, col + 2*j) == 0:
                        moves[(row + 2*i, col + 2*j)] = jumped + [first_piece]
                        moves.update(self._more_jumps_check(row + 2*i, col + 2*j, color, jumped + [first_piece]))
        return moves

    def _king_normal_moves(self, piece):
        moves = {}
        row = piece.row
        col = piece.col
        for i in [-1, 1]:
            for j in [-1, 1]:
                tmp = 1
                flag = True
                while flag:
                    first_piece = self.get_piece(row + i*tmp, col + j*tmp)
                    if first_piece == 0:
                        moves[(row + i*tmp, col + j*tmp)] = []
                        tmp += 1
                    else:
                        flag = False
        return moves

    def _king_takes(self, row, col, color, jumped):
        moves = {}
        for i in [-1, 1]:
            for j in [-1, 1]:
                tmp = 1
                flag = True
                while flag:
                    first_piece = self.get_piece(row + i * tmp, col + j * tmp)
                    if first_piece == 0:
                        tmp += 1
                    elif first_piece == -1 or first_piece.color == color:
                        flag = False
                    elif first_piece not in jumped:  # possible takes
                        flag2 = True
                        while flag2:
                            tmp += 1
                            second_piece = self.get_piece(row + i * tmp, col + j * tmp)
                            if second_piece == 0:
                                moves[(row + i * tmp, col + j * tmp)] = jumped + [first_piece]
                                moves.update(self._king_takes(row + i * tmp, col + j * tmp, color, jumped + [first_piece]))
                            else:
                                flag2 = False
                                flag = False
                    else:
                        flag = False
        return moves

    def calculate_all_moves(self, turn):
        all_moves = {}
        for rows in self.board:
            for piece in rows:
                if piece != 0 and piece != -1:
                    if piece.color == turn:
                        moves = self.get_valid_moves2(piece)
                        all_moves[piece] = moves
                        # for move in moves:
                        #     if piece in all_moves:
                        #         all_moves[piece] = all_moves[piece] + {move, moves[move]}
                        #     else:
                        #         all_moves[piece] = {move, moves[move]}
        all_moves_with_takes_rule = {}
        max_takes = 0
        for piece_moves in all_moves:
            for move in all_moves[piece_moves]:
                if len(all_moves[piece_moves][move]) > max_takes:
                    max_takes = len(all_moves[piece_moves][move])

        for piece_moves in all_moves:
            tmp = {}
            for move in all_moves[piece_moves]:
                if len(all_moves[piece_moves][move]) == max_takes:
                    tmp[move] = all_moves[piece_moves][move]
            if not tmp == {}:
                all_moves_with_takes_rule[piece_moves] = tmp

        key_arr = []
        for key in all_moves_with_takes_rule:
            key_arr.append(key)
        random.shuffle(key_arr)

        self.possible_moves = {}
        for key in key_arr:
            self.possible_moves[key] = all_moves_with_takes_rule[key]



        # self.possible_moves = all_moves_with_takes_rule
        # self.possible_moves = all_moves


    def get_valid_moves_from_all(self, piece):
        if piece in self.possible_moves:
            moves = self.possible_moves[piece]
            return moves
        return {}




    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row
        if piece.color == WHITE_PIECES or piece.king:
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))
        if piece.color == BLACK_PIECES or piece.king:
            moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right))

        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            current = self.get_piece(r, left)
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last

                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)

                    moves.update(self._traverse_left(r+step, row, step, color, left-1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, left + 1, skipped=last))
                break

            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1
        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break
            current = self.get_piece(r, right)
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)

                    moves.update(self._traverse_left(r + step, row, step, color, right - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, right + 1, skipped=last))
                break

            elif current.color == color:
                break
            else:
                last = [current]

            right += 1
        return moves

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece.color == WHITE_PIECES:
                self.white_left -= 1
            if piece.color == BLACK_PIECES:
                self.black_left -= 1

    def winner(self, turn):
        if self.king_moves_in_a_row == 15:
            return "REMIS"
        if self.black_left <= 0:
            return WHITE_PIECES
        elif self.white_left <= 0:
            return BLACK_PIECES
        if len(self.possible_moves) == 0:
            if turn == BLACK_PIECES:
                return WHITE_PIECES
            else:
                return WHITE_PIECES
        return None

    def ev_pawns_diff(self):
        return self.white_left - self.black_left

    def ev_kings_diff(self):
        return self.white_kings - self.black_kings

    def ev_center_diff(self):
        black_small_points = 0
        white_small_points = 0
        for i in range(8):
            for j in range(8):
                piece = self.get_piece(i, j)
                if piece != 0:
                    if piece.color == WHITE_PIECES:
                        if piece.row in [2, 3, 4, 5] and piece.col in [2, 3, 4, 5]:
                            white_small_points += 1
                    else:
                        if piece.row in [2, 3, 4, 5] and piece.col in [2, 3, 4, 5]:
                            black_small_points += 1
        return white_small_points - black_small_points

    def ev_zones(self):
        black_small_points = 0
        white_small_points = 0
        for i in range(8):
            for j in range(8):
                piece = self.get_piece(i, j)
                if piece != 0:
                    if piece.row in [0, 7] or piece.col in [0, 7]:
                        if piece.col == WHITE_PIECES:
                            white_small_points += 1
                        else:
                            black_small_points += 1
                    elif piece.row in [1, 6] or piece.col in [1, 6]:
                        if piece.col == WHITE_PIECES:
                            white_small_points += 2
                        else:
                            black_small_points += 2
                    else:
                        if piece.color == WHITE_PIECES:
                            white_small_points += 3
                        else:
                            black_small_points += 3
        return white_small_points - black_small_points

    def ev_edges_diff(self):
        white_counter = 0
        black_counter = 0
        for i in range(8):
            for j in range(8):
                piece = self.get_piece(i, j)
                if piece != 0:
                    if piece.row in [0,7] and piece.col in [0,7]:
                        if piece.color == WHITE_PIECES:
                            white_counter += 1
                        else:
                            black_counter += 1
        return white_counter - black_counter

    def ev_neighbours_diff(self):
        white_counter = 0
        black_counter = 0
        for i in range(8):
            for j in range(8):
                piece = self.get_piece(i, j)
                if piece != 0:
                    for m in [-1, 1]:
                        for n in [-1, 1]:
                            tmp_piece = self.get_piece(i+m, j+n)
                            if tmp_piece != 0 and tmp_piece != -1:
                                if tmp_piece.color == piece.color:
                                    if piece.color == WHITE_PIECES:
                                        white_counter += 1
                                    else:
                                        black_counter += 1
        return white_counter - black_counter



    def evaluate(self, player_number):
        if player_number == 1:
            return self.ev_pawns_diff() + self.ev_kings_diff() * 3  # 1
        elif player_number == 2:
            return self.ev_pawns_diff() + self.ev_kings_diff() * 5  # 2
        elif player_number == 3:
            return self.ev_pawns_diff() + self.ev_kings_diff() * 3 + self.ev_center_diff() * 0.6 + self.ev_neighbours_diff() * 0.6  # 3
        elif player_number == 4:
            return self.ev_pawns_diff() + self.ev_kings_diff() * 3 + self.ev_edges_diff() + self.ev_neighbours_diff() * 0.9  # 4
        elif player_number == 5:
            return self.ev_zones() + self.ev_kings_diff() * 2  # 5
        else:
            return self.ev_pawns_diff()



