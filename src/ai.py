# ai.py

import math
from random import choice

class AI:
    def __init__(self, game):
        self.game = game  # Reference to TicTacToe class
        self.ai_symbol = game.ai_symbol  # 'O' by default
        self.human_symbol = game.player_symbol  # 'X' by default

    def get_best_move(self, difficulty):
        available_moves = list(self.game.available_moves)
        if difficulty == 'easy':
            return choice(available_moves)
        elif difficulty == 'medium':
            # Medium difficulty: Try to win or block, else random
            move = self.find_winning_move()
            if move:
                return move
            move = self.find_blocking_move()
            if move:
                return move
            return choice(available_moves)
        elif difficulty == 'hard':
            # Hard difficulty: Use Minimax algorithm
            best_score = -math.inf
            best_move = None
            for move in available_moves:
                self.game.make_move(move, self.ai_symbol)
                score = self.minimax(False, -math.inf, math.inf)
                self.game.undo_move(move)
                if score > best_score:
                    best_score = score
                    best_move = move
            return best_move

    def find_winning_move(self):
        for move in self.game.available_moves:
            self.game.make_move(move, self.ai_symbol)
            if self.game.check_winner_cache() == self.ai_symbol:
                self.game.undo_move(move)
                return move
            self.game.undo_move(move)
        return None

    def find_blocking_move(self):
        for move in self.game.available_moves:
            self.game.make_move(move, self.human_symbol)
            if self.game.check_winner_cache() == self.human_symbol:
                self.game.undo_move(move)
                return move
            self.game.undo_move(move)
        return None

    def minimax(self, is_maximizing, alpha, beta):
        winner = self.game.check_winner_cache()
        if winner == self.ai_symbol:
            return 1
        elif winner == self.human_symbol:
            return -1
        elif self.game.is_board_full():
            return 0

        if is_maximizing:
            max_eval = -math.inf
            for move in list(self.game.available_moves):
                self.game.make_move(move, self.ai_symbol)
                eval = self.minimax(False, alpha, beta)
                self.game.undo_move(move)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = math.inf
            for move in list(self.game.available_moves):
                self.game.make_move(move, self.human_symbol)
                eval = self.minimax(True, alpha, beta)
                self.game.undo_move(move)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval
