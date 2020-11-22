import time

import pygame
from math import ceil
from random import shuffle

# local imports
from cards import Deck
from board import Board
from constants import *
from player import Player
from non_playable_character import simpleBot


class Durak:
    def __init__(self, pygame_clock, game_controller):
        self.dt = 0
        self.pygame_clock, self.game_controller = pygame_clock, game_controller
        self.deck = Deck()
        self.load_image_assets()
        self.board = Board(pygame_clock, self.deck)
        self.back_image = self.deck.cards_list[-1].current_image.copy()
        self.deck_x, self.deck_y = (SCREENWIDTH // 2), (SCREENHEIGHT // 2) - (self.back_image.get_rect().size[1] // 2)

        # mouse + position
        self.click = False
        self.mx, self.my = 0, 0

        self.were_init_cards_dealt = False

        self.animating_init_deck = True
        self.animating_init_deal = False

        self.show_card_size = False

        self.animate_deck_count = 1 # used in self.animate_init_deck
        self.animate_init_deal_count = 0 # used in deal_cards_init_animation

        self.players = []
        self.player_count = 0
        self.attacker = None

        self.add_player(Player("Alex", True, 0))
        self.add_player(simpleBot("NPC837", 1))
        self.add_player(simpleBot("NPC619", 2))

    def update(self):
        self.mx, self.my = pygame.mouse.get_pos()
        if not self.animating_init_deck and not self.were_init_cards_dealt:
            self.init_card_deal()
            self.were_init_cards_dealt = True

        if self.click:
            self.show_card_size = not self.show_card_size
            print(self.mx, self.my)
            self.click = False

    def mouse_click(self):
        self.click = True

    # Game --------------------------------------------------------------------------------------------------------
    def get_first_attacker(self):
        temp_player, lowest_card = None, None
        # shuffle self.players so that if two players have 2s, one is randomly chosen
        temp_players = self.players.copy()
        shuffle(temp_players)
        for p in temp_players:
            p_lowest = p.get_lowest_card()
            if lowest_card is None or (lowest_card.uber and not p_lowest.uber):
                lowest_card = p_lowest
                temp_player = p
            elif lowest_card.uber == p_lowest.uber and p_lowest.rank < lowest_card.rank:
                lowest_card = p_lowest
                temp_player = p
        print("{} is the attacker because of {}".format(temp_player.name, lowest_card))
        self.attacker = temp_player

    def init_card_deal(self):
        # deal card by card
        for i in range(6):
            for p in self.players:
                if p.need_more_cards():
                    p.draw_card(self.deck.pop())
                    p.sort_hand()
        self.get_first_attacker()

    def load_image_assets(self):
        for c in self.deck.cards_list:
            c.load_image_assets()

    def add_player(self, player):
        self.players.append(player)
        self.player_count += 1

    # Draw and Animate---------------------------------------------------------------------------------------------
    def render(self, screen):
        self.dt = self.pygame_clock.tick(60) / 1000.0
        # for now just render board all the time
        if self.animating_init_deck:
            self.animating_init_deck = self.animate_init_deck(screen)
            self.animating_init_deal = not self.animating_init_deck
        elif self.animating_init_deal:
            self.draw_deck(screen)
            self.animating_init_deal = self.animate_init_deal(screen)
        else:
            self.draw_deck(screen)
            self.draw_players(screen)
            # Eventually just call from this point
            self.board.render(screen)

        self.board.render(screen)
        # DRAW A RECT
        if self.show_card_size:
            temp_rect = pygame.rect.Rect(self.mx, self.my, self.back_image.get_rect().size[0], self.back_image.get_rect().size[1])
            pygame.draw.rect(screen, (255, 255, 255), temp_rect)


    def draw_players(self, screen):
        for p in self.players:
            if p.is_user:
                user_cards_x = SCREENWIDTH // 4
                user_cards_x_end = SCREENWIDTH - SCREENWIDTH // 4
                user_cards_gap = (user_cards_x_end - user_cards_x) / len(p)
                for i, c in enumerate(p.hand):
                    # temp_card = self.back_card.copy()
                    temp_card = c.current_image
                    # temp_card = self.deckImages.get(c.suit + str(c.rank))
                    temp_card_height = temp_card.get_rect().size[1]
                    screen.blit(temp_card,
                                (user_cards_x + i * user_cards_gap, SCREENHEIGHT - temp_card_height // 2))
            elif p.id == 1:
                # Left user
                user_cards_y = SCREENHEIGHT // 4
                user_cards_y_end = SCREENHEIGHT - SCREENHEIGHT // 4
                user_cards_gap = (user_cards_y_end - user_cards_y) / len(p)
                for i, c in enumerate(p.hand):
                    temp_card = c.current_image
                    temp_card = pygame.transform.rotate(temp_card, 90)
                    temp_card_width = temp_card.get_rect().size[0]
                    screen.blit(temp_card, (-((temp_card_width * 2) // 3), user_cards_y + i * user_cards_gap))
            elif p.id == 2:
                # Right user
                user_cards_y = SCREENHEIGHT // 4
                user_cards_y_end = SCREENHEIGHT - SCREENHEIGHT // 4
                user_cards_gap = (user_cards_y_end - user_cards_y) / len(p)
                for i, c in enumerate(p.hand):
                    temp_card = c.current_image
                    temp_card = pygame.transform.rotate(temp_card, 90)
                    temp_card_width = temp_card.get_rect().size[0]
                    screen.blit(temp_card, (SCREENWIDTH - temp_card_width // 3, user_cards_y + i * user_cards_gap))

    def draw_deck(self, screen):
        back_c_image = self.deck.cards_list[-1].back_image
        for i in range(ceil(len(self.deck) / 4.5)):
            screen.blit(back_c_image, (self.deck_x + i * 2, self.deck_y + i * 2))

        top_card_image = self.deck.top_card.front_image
        screen.blit(top_card_image, (self.deck_x - top_card_image.get_rect().size[0], self.deck_y))

        return True
        # self.screen.blit(topCard, (deckX - cardWidth - 5, deckY))

    def animate_init_deal(self, screen):
        # animate one card at a time. self.deal_cards_init_animation_count is our index
        if self.animate_init_deal_count < 6 * self.player_count:
            player_index = self.animate_init_deal_count % self.player_count
            card_index = self.animate_init_deal_count // self.player_count
            card_dealt = self.players[player_index].hand[card_index]
            card_width, card_height = card_dealt.current_image.get_rect().size

            if player_index % 3 == 0:
                card_goal_x, card_goal_y = SCREENWIDTH // 2 - card_width // 2, SCREENHEIGHT - card_height // 2
                card_goal_rotate = 0
            elif player_index % 3 == 1:
                card_goal_x, card_goal_y = -(card_height // 2), SCREENHEIGHT // 2 - card_width // 2
                card_goal_rotate = 90
            elif player_index % 3 == 2:
                card_goal_x, card_goal_y = SCREENWIDTH - card_height // 2, SCREENHEIGHT // 2 - card_width // 2
                card_goal_rotate = 90
            else:
                card_goal_x, card_goal_y = SCREENWIDTH // 2, SCREENHEIGHT // 2
                card_goal_rotate = 0

            if self.animate_init_deal_count >= 1:
                user_x, user_y = SCREENWIDTH // 2 - card_width // 2, SCREENHEIGHT - card_height // 2
                screen.blit(card_dealt.current_image, (user_x, user_y))
            if self.animate_init_deal_count >= 2:
                left_x, left_y = -(card_height // 2), SCREENHEIGHT // 2 - card_width // 2
                temp_screen = pygame.transform.rotate(card_dealt.current_image, 90)
                screen.blit(temp_screen, (left_x, left_y))
            if self.animate_init_deal_count >= 3:
                right_x, right_y = SCREENWIDTH - card_height // 2, SCREENHEIGHT // 2 - card_width // 2
                temp_screen = pygame.transform.rotate(card_dealt.current_image, 270)
                screen.blit(temp_screen, (right_x, right_y))

            if card_dealt.is_animating:
                card_screen = card_dealt.update_pos()
                screen.blit(card_screen, card_dealt.c_pos)
                if card_dealt.c_pos == card_dealt.g_pos:
                    self.animate_init_deal_count += 1
            else:
                card_dealt.set_new_pos((self.deck_x, self.deck_y), (card_goal_x, card_goal_y), card_goal_rotate)
                screen.blit(card_dealt.current_image, card_dealt.c_pos)

        # @ card count == player_count * 6 (launch animation)
        if self.animate_init_deal_count == self.player_count * 6:
            for p_index, p in enumerate(self.players):
                for i, c in enumerate(p.hand):
                    card_width, card_height = c.current_image.get_rect().size
                    if p_index == 0:
                        user_x = SCREENWIDTH // 2 - card_width // 2
                        user_y = SCREENHEIGHT - card_height // 2
                        user_cards_gap = ((SCREENWIDTH - SCREENWIDTH // 4) - (SCREENWIDTH // 4)) / len(self.players[0])
                        user_goal_x = round(SCREENWIDTH // 4 + i * user_cards_gap)
                        user_goal_y = SCREENHEIGHT - card_height // 2
                        c.set_new_pos((user_x, user_y), (user_goal_x, user_goal_y))
                    elif p_index == 1:
                        left_x = -(card_height // 2)
                        left_y = SCREENHEIGHT // 2 - card_width // 2
                        left_cards_gap = ((SCREENHEIGHT - SCREENHEIGHT // 4) - (SCREENHEIGHT // 4)) / len(p)
                        left_goal_x = -((card_height * 2) // 3)
                        left_goal_y = round((SCREENHEIGHT // 4) + i * left_cards_gap)
                        c.set_new_pos((left_x, left_y), (left_goal_x, left_goal_y), 90)
                    elif p_index == 2:
                        right_x = SCREENWIDTH - card_height // 2
                        right_y = SCREENHEIGHT // 2 - card_width // 2
                        right_cards_gap = ((SCREENHEIGHT - SCREENHEIGHT // 4) - (SCREENHEIGHT // 4)) / len(p)
                        right_goal_x = SCREENWIDTH - card_height // 3
                        right_goal_y = round((SCREENHEIGHT // 4) + i * right_cards_gap)
                        c.set_new_pos((right_x, right_y), (right_goal_x, right_goal_y), 90)
            self.animate_init_deal_count += 1

        # @ card count == player_count * 6 + 1 (update animation)
        if self.animate_init_deal_count == self.player_count * 6 + 1:

            for p in self.players:
                for c in p.hand:
                    screen.blit(c.update_pos(6), c.c_pos)

            if all(not c.is_animating for c in self.players[0].hand):
                if all(not c.is_animating for c in self.players[1].hand):
                    if all(not c.is_animating for c in self.players[2].hand):
                        self.animate_init_deal_count += 1

        if self.animate_init_deal_count >= self.player_count * 6 + 2:
            for i in range(len(self.players)):
                for j, c in enumerate(self.players[i].hand):
                    screen.blit(c.update_pos(6), c.c_pos)
                    if i == 0 and c.c_flip == 0 and j <= (self.animate_init_deal_count - self.player_count * 6 - 2) // 2:
                        c.flip_card()
            self.animate_init_deal_count += 1
            if all(not c.is_animating for c in self.players[0].hand):
                return False
        return True

    def animate_init_deck(self, screen):
        back_card_image = self.deck.cards_list[0].back_image
        card_width, card_height = back_card_image.get_rect().size
        for i in range(6):
            if i == self.animate_deck_count // 3:
                self.animate_deck_count += 1
                return True
            screen.blit(back_card_image, (self.deck_x + i * 2, self.deck_y + i * 2))
        # we've animated it all
        self.animate_deck_count = 1
        return False