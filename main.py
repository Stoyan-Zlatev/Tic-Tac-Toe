# main.py

import pygame as pg
import os
import sys
from game_logic import TicTacToe

os.environ['SDL_AUDIODRIVER'] = 'dsp'  # Set a dummy audio driver to suppress ALSA errors


WIN_SIZE = 600

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode([WIN_SIZE] * 2)
        self.clock = pg.time.Clock()
        self.tic_tac_toe = None  # Will be initialized in new_game
        self.menu_state = 'main_menu'  # 'main_menu', 'difficulty_menu', 'choose_starter', 'game'
        self.game_mode = None  # 'human', 'easy', 'medium', 'hard'
        self.player_starts = True  # Default player starts

    def new_game(self):
        if self.game_mode == 'human':
            self.tic_tac_toe = TicTacToe(self, game_mode='human', player_starts=self.player_starts)
        else:
            self.tic_tac_toe = TicTacToe(self, game_mode='ai', difficulty=self.game_mode, player_starts=self.player_starts)

    def show_main_menu(self):
        self.screen.fill((0, 0, 0))
        font = pg.font.SysFont('Verdana', 40, True)
        label = font.render('Tic Tac Toe', True, 'white')
        self.screen.blit(label, (WIN_SIZE // 2 - label.get_width() // 2, WIN_SIZE // 4))
        font = pg.font.SysFont('Verdana', 30, True)
        label1 = font.render('1. Player vs Player', True, 'white')
        label2 = font.render('2. Player vs Computer', True, 'white')
        self.screen.blit(label1, (WIN_SIZE // 2 - label1.get_width() // 2, WIN_SIZE // 2))
        self.screen.blit(label2, (WIN_SIZE // 2 - label2.get_width() // 2, WIN_SIZE // 2 + 50))
        pg.display.set_caption('Main Menu')

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_1:
                    self.game_mode = 'human'
                    self.new_game()
                    self.menu_state = 'game'
                elif event.key == pg.K_2:
                    self.menu_state = 'choose_starter'

    def show_choose_starter_menu(self):
        self.screen.fill((0, 0, 0))
        font = pg.font.SysFont('Verdana', 40, True)
        label = font.render('Who should start?', True, 'white')
        self.screen.blit(label, (WIN_SIZE // 2 - label.get_width() // 2, WIN_SIZE // 4))
        font = pg.font.SysFont('Verdana', 30, True)
        label1 = font.render('1. Player Starts', True, 'white')
        label2 = font.render('2. Computer Starts', True, 'white')
        self.screen.blit(label1, (WIN_SIZE // 2 - label1.get_width() // 2, WIN_SIZE // 2))
        self.screen.blit(label2, (WIN_SIZE // 2 - label2.get_width() // 2, WIN_SIZE // 2 + 50))
        pg.display.set_caption('Choose Starter')

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_1:
                    self.player_starts = True
                    self.menu_state = 'difficulty_menu'
                elif event.key == pg.K_2:
                    self.player_starts = False
                    self.menu_state = 'difficulty_menu'

    def show_difficulty_menu(self):
        self.screen.fill((0, 0, 0))
        font = pg.font.SysFont('Verdana', 40, True)
        label = font.render('Choose Difficulty', True, 'white')
        self.screen.blit(label, (WIN_SIZE // 2 - label.get_width() // 2, WIN_SIZE // 4))
        font = pg.font.SysFont('Verdana', 30, True)
        label1 = font.render('1. Easy', True, 'white')
        label2 = font.render('2. Medium', True, 'white')
        label3 = font.render('3. Hard', True, 'white')
        self.screen.blit(label1, (WIN_SIZE // 2 - label1.get_width() // 2, WIN_SIZE // 2))
        self.screen.blit(label2, (WIN_SIZE // 2 - label2.get_width() // 2, WIN_SIZE // 2 + 50))
        self.screen.blit(label3, (WIN_SIZE // 2 - label3.get_width() // 2, WIN_SIZE // 2 + 100))
        pg.display.set_caption('Difficulty Menu')

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_1:
                    self.game_mode = 'easy'
                    self.new_game()
                    self.menu_state = 'game'
                elif event.key == pg.K_2:
                    self.game_mode = 'medium'
                    self.new_game()
                    self.menu_state = 'game'
                elif event.key == pg.K_3:
                    self.game_mode = 'hard'
                    self.new_game()
                    self.menu_state = 'game'
                elif event.key == pg.K_ESCAPE:
                    self.menu_state = 'main_menu'

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.new_game()
                elif event.key == pg.K_ESCAPE and self.menu_state == 'game':
                    # Switch back to main menu if Esc is pressed during the game
                    self.menu_state = 'main_menu'

    def run(self):
        while True:
            if self.menu_state == 'main_menu':
                self.show_main_menu()
            elif self.menu_state == 'choose_starter':
                self.show_choose_starter_menu()
            elif self.menu_state == 'difficulty_menu':
                self.show_difficulty_menu()
            elif self.menu_state == 'game':
                self.tic_tac_toe.run()
                self.check_events()
            pg.display.update()
            self.clock.tick(60)


if __name__ == '__main__':
    game = Game()
    game.run()
