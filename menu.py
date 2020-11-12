import pygame
from constants import *

from math import log


class Menu:
    def __init__(self, pygame_clock):
        # Get clock so we can do dt animation math
        self.pygame_clock = pygame_clock

        # load fonts, for now assume same fonts, different variables
        self.titleFont = pygame.font.Font('Res/Font/CozetteVector.ttf', 128)
        self.buttonFont = pygame.font.Font('Res/Font/CozetteVector.ttf', 64)

        # create all text objects we'll need to draw
        self.titleText = self.titleFont.render("Durak", False, (255, 255, 255)).convert()
        self.startText = self.buttonFont.render("Start", False, (0, 0, 0)).convert()
        self.optionsText = self.buttonFont.render("Options", False, (0, 0, 0)).convert()

        self.startTextSize = self.buttonFont.size("Start")
        self.optionsTextSize = self.buttonFont.size("Options")

        # aspirational button_width, button_x location defined by ScreenWidth
        button_width = SCREENWIDTH - (SCREENWIDTH // 2)
        self.button_x = button_width - button_width // 2

        self.titleX = SCREENWIDTH // 2 - (self.titleFont.size("Durak")[0] // 2)
        self.titleY = -260

        # create buttons for our menu
        self.startButton = pygame.Rect(SCREENWIDTH + 200, 200, button_width, 75)
        self.optionsButton = pygame.Rect(SCREENWIDTH + 200, 350, button_width, 75)

        self.button_frame_count = 0
        self.title_frame_count = 0

        # mouse position
        self.mx = 0
        self.my = 0

        self.dt = 0

        self.state = MENU_SCREEN
        self.click = False

    def update(self):
        self.dt = self.pygame_clock.tick(60) / 1000.0
        if self.state == MENU_SCREEN:
            self.animate_buttons_on_screen()
            self.animate_title_on_screen()
        else:
            pass
        self.mx, self.my = pygame.mouse.get_pos()

    def render(self, screen):
        screen.blit(self.titleText, (self.titleX, self.titleY))
        pygame.draw.rect(screen, (255, 255, 255), self.startButton)
        screen.blit(self.startText, (self.startButton.centerx - self.startTextSize[0] // 2, self.startButton.y))
        pygame.draw.rect(screen, (255, 255, 255), self.optionsButton)
        screen.blit(self.optionsText, (self.optionsButton.centerx - self.optionsTextSize[0] // 2, self.optionsButton.y))

    def mouse_click(self):
        self.click = True

    def get_menu_click(self):
        if self.startButton.collidepoint(self.mx, self.my):
            self.state = GAME_SCREEN
            return GAME_SCREEN
        if self.optionsButton.collidepoint(self.my, self.my):
            self.state = OPTION_SCREEN
            return OPTION_SCREEN
        return 0

    def animate_off(self):
        self.animate_buttons_off_screen()
        self.animate_title_off_screen()

        # return the last button falling off screen to change screen
        return self.optionsButton.left >= SCREENWIDTH + 200

    def animate_buttons_off_screen(self):
        start_button_x_velocity = int(self.dt * self.button_frame_count)
        self.startButton.move_ip(start_button_x_velocity, 0)

        options_button_x_velocity = 0 if self.button_frame_count <= 600 else int(self.dt * self.button_frame_count)
        self.optionsButton.move_ip(options_button_x_velocity, 0)

        self.button_frame_count += 40

    def animate_buttons_on_screen(self):
        if self.startButton.x > self.button_x:
            if self.dt < 1:
                start_button_x_velocity = -int(1 + self.dt * (1.4 * self.startButton.x - self.button_x))
                self.startButton.move_ip(start_button_x_velocity, 0)

        if self.optionsButton.x > self.button_x and self.startButton.x <= self.button_x * 3:
            if self.dt < 1:
                options_button_x_velocity = -int(1 + self.dt * (1.4 * self.optionsButton.x - self.button_x))
                self.optionsButton.move_ip(options_button_x_velocity, 0)

    def animate_title_on_screen(self):
        if self.titleY <= 0:
            if self.titleY <= -100:
                self.titleY += 6
            elif self.titleY <= -20:
                self.titleY += 4
            else:
                self.titleY += 1

    def animate_title_off_screen(self):
        # Needs to be tested More
        if self.titleY >= -260:
            if self.titleY > -20:
                self.titleY -= 2
            elif self.titleY > -100:
                self.titleY -= 4
            else:
                self.titleY -= 6
