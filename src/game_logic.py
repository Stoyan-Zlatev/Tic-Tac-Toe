# game_logic.py

import pygame as pg
import sys
from random import randint
from ai import AI

WIN_SIZE = 600
CELL_SIZE = WIN_SIZE // 3
INF = float('inf')
vec2 = pg.math.Vector2
CELL_CENTER = vec2(CELL_SIZE / 2)


class TicTacToe:
    def __init__(self, game, game_mode='human', difficulty='easy', player_starts=True):
        self.game = game
        self.field_image = self.get_scaled_image(path='./assets/images/field.png', res=[WIN_SIZE] * 2)
        self.O_image = self.get_scaled_image(path='./assets/images/o.png', res=[CELL_SIZE] * 2)
        self.X_image = self.get_scaled_image(path='./assets/images/x.png', res=[CELL_SIZE] * 2)

        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.available_moves = {(i, j) for i in range(3) for j in range(3)}
        self.cache = {
            "rows": [0, 0, 0],
            "cols": [0, 0, 0],
            "diag1": 0,
            "diag2": 0
        }

        self.player_symbol = 'X'  # Human player symbol
        self.ai_symbol = 'O'  # AI player symbol
        self.current_player = self.player_symbol if player_starts else self.ai_symbol

        self.winner = None
        self.winner_line = None
        self.game_steps = 0
        self.font = pg.font.SysFont('Verdana', CELL_SIZE // 4, True)

        self.game_mode = game_mode  # 'human' or 'ai'
        self.difficulty = difficulty  # 'easy', 'medium', 'hard'

        self.AI = None
        if self.game_mode != 'human':
            self.AI = AI(self)

    def check_winner_cache(self) -> str:
        all_sums = self.cache["rows"] + self.cache["cols"] + [self.cache["diag1"], self.cache["diag2"]]
        if any(value == 3 for value in all_sums):
            return 'X'  # Human player wins
        elif any(value == -3 for value in all_sums):
            return 'O'  # AI wins
        return None

    def is_board_full(self) -> bool:
        return len(self.available_moves) == 0

    def make_move(self, move, player_symbol):
        i, j = move
        self.board[i][j] = player_symbol
        self.available_moves.remove(move)

        value = 1 if player_symbol == 'X' else -1
        self.cache["rows"][i] += value
        self.cache["cols"][j] += value
        if i == j:
            self.cache["diag1"] += value
        if i + j == 2:
            self.cache["diag2"] += value

    def undo_move(self, move):
        i, j = move
        player_symbol = self.board[i][j]
        self.board[i][j] = ' '
        self.available_moves.add(move)

        value = 1 if player_symbol == 'X' else -1
        self.cache["rows"][i] -= value
        self.cache["cols"][j] -= value
        if i == j:
            self.cache["diag1"] -= value
        if i + j == 2:
            self.cache["diag2"] -= value

    def run_game_process(self):
        if self.winner:
            return

        if self.game_mode == 'human' or self.current_player == self.player_symbol:
            # Human player's turn
            current_cell = vec2(pg.mouse.get_pos()) // CELL_SIZE
            row, col = int(current_cell.y), int(current_cell.x)  # Fixed: match row and col correctly
            left_click = pg.mouse.get_pressed()[0]

            if left_click and (row, col) in self.available_moves:
                self.make_move((row, col), self.current_player)
                self.game_steps += 1
                self.winner = self.check_winner_cache()
                if self.winner:
                    self.get_winner_line()
                elif self.is_board_full():
                    self.winner = 'Draw'
                else:
                    self.switch_player()
        else:
            # AI player's turn
            pg.time.wait(50)  # small delay for better experience
            move = self.AI.get_best_move(self.difficulty)
            if move:
                self.make_move(move, self.current_player)
                self.game_steps += 1
                self.winner = self.check_winner_cache()
                if self.winner:
                    self.get_winner_line()
                elif self.is_board_full():
                    self.winner = 'Draw'
                else:
                    self.switch_player()

    def switch_player(self):
        self.current_player = self.player_symbol if self.current_player == self.ai_symbol else self.ai_symbol

    def get_winner_line(self):
        # Implement the logic to get the winning line for drawing purposes
        lines = [
            [(0, 0), (0, 1), (0, 2)],  # Rows
            [(1, 0), (1, 1), (1, 2)],
            [(2, 0), (2, 1), (2, 2)],
            [(0, 0), (1, 0), (2, 0)],  # Columns
            [(0, 1), (1, 1), (2, 1)],
            [(0, 2), (1, 2), (2, 2)],
            [(0, 0), (1, 1), (2, 2)],  # Diagonals
            [(0, 2), (1, 1), (2, 0)]
        ]
        for line in lines:
            values = [self.board[i][j] for i, j in line]
            if values == [self.winner]*3:
                self.winner_line = [vec2(line[0][::-1]) * CELL_SIZE + CELL_CENTER,
                                    vec2(line[2][::-1]) * CELL_SIZE + CELL_CENTER]
                break

    def draw_objects(self):
        for i in range(3):
            for j in range(3):
                symbol = self.board[i][j]
                if symbol != ' ':
                    img = self.X_image if symbol == 'X' else self.O_image
                    self.game.screen.blit(img, vec2(j, i) * CELL_SIZE)

    def draw_winner(self):
        if self.winner and self.winner != 'Draw':
            pg.draw.line(self.game.screen, 'red', *self.winner_line, CELL_SIZE // 8)
            label = self.font.render(f'Player "{self.winner}" wins!', True, 'white', 'black')
            self.game.screen.blit(label, (WIN_SIZE // 2 - label.get_width() // 2, WIN_SIZE // 4))
        elif self.winner == 'Draw':
            label = self.font.render(f"It's a draw!", True, 'white', 'black')
            self.game.screen.blit(label, (WIN_SIZE // 2 - label.get_width() // 2, WIN_SIZE // 4))

    def draw(self):
        self.game.screen.blit(self.field_image, (0, 0))
        self.draw_objects()
        self.draw_winner()

    @staticmethod
    def get_scaled_image(path, res):
        img = pg.image.load(path)
        return pg.transform.smoothscale(img, res)

    def print_caption(self):
        if self.winner:
            if self.winner == 'Draw':
                pg.display.set_caption(f"It's a draw! Press Space to Restart")
            elif self.game_mode != 'human' and self.winner == self.ai_symbol:
                pg.display.set_caption(f'Computer ("{self.winner}") wins! Press Space to Restart')
            else:
                pg.display.set_caption(f'Player "{self.winner}" wins! Press Space to Restart')
        else:
            if self.game_mode == 'human':
                pg.display.set_caption(f'Player "{self.current_player}" turn!')
            else:
                if self.current_player == self.ai_symbol:
                    pg.display.set_caption(f'Computer ("{self.current_player}") turn!')
                else:
                    pg.display.set_caption(f'Your ("{self.current_player}") turn!')

    def run(self):
        self.print_caption()
        self.draw()
        self.run_game_process()
