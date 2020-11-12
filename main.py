import time

import pygame
from pygame.locals import *

# Local imports
from constants import *
from durak_game import Durak
from menu import Menu

class MainController:
    def __init__(self):
        # Create pygame instance, set screen, clock
        pygame.init()
        pygame.display.set_caption("Durak")
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        self.clock = pygame.time.Clock()
        self.clock.tick(60)

        self.debugFont = pygame.font.SysFont("Arial", 18)

        # screen_state decides what the screen should be aspirationally displaying
        self.screen_state = MENU_SCREEN
        # animate_state decides what we are currently animating
        self.animate_state = MENU_SCREEN

        self.game_created = False

        self.background, self.game = None, None
        self.menu = Menu(self.clock)

        self.set_background()

    def set_background(self):
        self.background = pygame.surface.Surface(SCREENSIZE)
        self.background.fill(GREEN)

    # Start Game
    def start_game(self):
        self.game = Durak(self.clock, self)

    # Update
    def update(self):
        self.check_events()
        if self.screen_state == MENU_SCREEN:
            self.menu.update()
        elif self.screen_state == GAME_SCREEN:
            # create and start game
            if not self.game_created:
                self.start_game()
                self.game_created = True
            self.game.update()
        self.render()

    # Check Events
    def check_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == MOUSEBUTTONDOWN:
                if self.animate_state == MENU_SCREEN:
                    self.menu.mouse_click()
                    self.animate_state = self.menu.get_menu_click()

    # Render
    def render(self):
        self.screen.blit(self.background, (0, 0))
        if self.screen_state == GAME_SCREEN:
            self.game.render(self.screen)
            # "kill" our menu if we don't need it
            if self.menu is not None:
                self.menu = None
        if self.animate_state == MENU_SCREEN:
            self.menu.render(self.screen)
        elif self.animate_state == GAME_SCREEN:
            # animate menu off screen while screen_state waits
            if self.screen_state == MENU_SCREEN:
                self.menu.render(self.screen)
                self.screen_state = self.menu.animate_off()
        self.draw_FPS()
        pygame.display.update()

    def draw_FPS(self):
        self.screen.blit(self.debugFont.render(str(round(self.clock.get_fps())), False, (255, 255, 0)), (15, 0))


if __name__ == '__main__':
    main_window = MainController()
    while True:
        main_window.update()
