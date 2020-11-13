import pygame
from math import ceil
from random import shuffle

# local imports
from cards import Deck, Card
from constants import *
from player import Player


class Durak:
    def __init__(self, pygame_clock, game_controller):
        self.pygame_clock = pygame_clock
        self.game_controller = game_controller
        self.gameDeck = Deck()
        self.deckImages = {}
        self.load_image_assets()
        self.debugPrint = True

        self.were_init_cards_dealt = False

        self.dt = 0
        self.back_card = self.deckImages.get("back")
        self.deck_x, self.deck_y = 0, 0

        self.currently_animating_deck = True
        self.currently_animating_init_deal = False

        # used in self.animate_init_deck
        self.animate_deck_cards_count = 1

        # used in deal_cards_init_animation
        self.deal_cards_init_animation_count = 0

        self.players = []
        self.attacker = None

        self.add_player(Player("Alex", True, 0))
        self.add_player(Player("NPC837", False, 1))
        self.add_player(Player("NPC619", False, 2))

    def get_first_attacker(self):
        temp_player = None
        lowest_card = None

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

    def load_image_assets(self):
        for c in self.gameDeck.cards_list:
            c.load_image_assets()

    def add_player(self, player):
        self.players.append(player)

    def deal_cards_init(self):
        # deal card by card
        for i in range(6):
            for p in self.players:
                if p.need_more_cards():
                    p.draw_card(self.gameDeck.pop())
                    p.sort_hand()
        self.get_first_attacker()

    def update(self):
        if not self.currently_animating_deck and not self.were_init_cards_dealt:
            self.deal_cards_init()
            self.were_init_cards_dealt = True

    def render(self, screen):
        self.dt = self.pygame_clock.tick(60) / 1000.0
        if self.currently_animating_deck:
            self.currently_animating_deck = self.animate_init_deck(screen)
            self.currently_animating_init_deal = not self.currently_animating_deck
        elif self.currently_animating_init_deal:
            self.draw_deck(screen)
            self.currently_animating_init_deal = self.deal_cards_init_animation(screen)
        else:
            self.draw_deck(screen)
            self.draw_players(screen)

    def draw_deck(self, screen):
        back_card_image = self.gameDeck.cards_list[1].back_card_image
        cardWidth, cardHeight = back_card_image.get_rect().size
        local_deck_x = (SCREENWIDTH // 2)
        local_deck_y = (SCREENHEIGHT // 2) - (cardHeight // 2)

        for i in range(ceil(len(self.gameDeck) / 4.5)):
            self.deck_x, self.deck_y = (local_deck_x + i * 2, local_deck_y + i * 2)
            screen.blit(back_card_image, (self.deck_x, self.deck_y))

        top_card_image = self.gameDeck.cards_list[-1].card_image
        screen.blit(top_card_image, (local_deck_x - top_card_image.get_rect().size[0], local_deck_y))

        return True
        # self.screen.blit(topCard, (deckX - cardWidth - 5, deckY))

    def deal_cards_init_animation(self, screen):
        temp_card = self.gameDeck.cards_list[1].back_card_image.copy()
        temp_card_width, temp_card_height = temp_card.get_rect().size
        user_y_pos = SCREENHEIGHT - temp_card_height // 2
        user_x_pos = SCREENWIDTH // 2 - temp_card_width // 2
        self.deck_x = (SCREENWIDTH // 2) + ceil(len(self.gameDeck) / 4.5)
        self.deck_y = (SCREENHEIGHT // 2) - (temp_card_width // 2) + ceil(len(self.gameDeck) / 4.5)

        # create len(players) * 6 cards, and deal them out

        # get first card and move it

        alex_card = self.players[0].hand[self.deal_cards_init_animation_count]

        if self.deal_cards_init_animation_count >= 1:
            screen.blit(alex_card.back_card_image, (user_x_pos, user_y_pos))


        if alex_card.is_animating:
            alex_card.update_pos()
            screen.blit(alex_card.back_card_image, (alex_card.current_position))
            if alex_card.current_position == alex_card.goal_position:
                self.deal_cards_init_animation_count += 1
                alex_card.is_animating = False
        else:
            self.animate_card(screen, alex_card, (self.deck_x, self.deck_y), (user_x_pos, user_y_pos))
            screen.blit(alex_card.back_card_image, (alex_card.current_position))



        return self.deal_cards_init_animation_count != 6

    def animate_card(self, screen, card, start, end, rotation = 0):
        card.current_position = start
        card.goal_position = end
        card.is_animating = True

        # still need to deal with angle rotation

    def animate_init_deck(self, screen):
        back_card_image = self.gameDeck.cards_list[0].back_card_image
        cardWidth, cardHeight = back_card_image.get_rect().size
        deckX = (SCREENWIDTH // 2)
        deckY = (SCREENHEIGHT // 2) - (cardHeight // 2)
        for i in range(6):
            if i == self.animate_deck_cards_count // 3:
                self.animate_deck_cards_count += 1
                return True
            screen.blit(back_card_image, (deckX + i * 2, deckY + i * 2))
        # we've animated it all
        self.animate_deck_cards_count = 1
        return False

    def draw_players(self, screen):
        for p in self.players:
            if p.is_user:
                user_cards_x = SCREENWIDTH // 4
                user_cards_x_end = SCREENWIDTH - SCREENWIDTH // 4
                user_cards_gap = (user_cards_x_end - user_cards_x) / len(p)
                for i, c in enumerate(p.hand):
                    # temp_card = self.back_card.copy()
                    temp_card = c.card_image
                    # temp_card = self.deckImages.get(c.suit + str(c.rank))
                    temp_card_height = temp_card.get_rect().size[1]
                    screen.blit(temp_card, (user_cards_x + i * user_cards_gap, SCREENHEIGHT - temp_card_height // 2))
            elif p.id == 1:
                # Left user
                user_cards_y = SCREENHEIGHT // 4
                user_cards_y_end = SCREENHEIGHT - SCREENHEIGHT // 4
                user_cards_gap = (user_cards_y_end - user_cards_y) / len(p)
                for i, c in enumerate(p.hand):
                    temp_card = c.back_card_image
                    temp_card = pygame.transform.rotate(temp_card, 90)
                    temp_card_width = temp_card.get_rect().size[0]
                    screen.blit(temp_card, (-((temp_card_width * 2) // 3), user_cards_y + i * user_cards_gap))
            elif p.id == 2:
                # Right user
                user_cards_y = SCREENHEIGHT // 4
                user_cards_y_end = SCREENHEIGHT - SCREENHEIGHT // 4
                user_cards_gap = (user_cards_y_end - user_cards_y) / len(p)
                for i, c in enumerate(p.hand):
                    temp_card = c.back_card_image
                    temp_card = pygame.transform.rotate(temp_card, 90)
                    temp_card_width = temp_card.get_rect().size[0]
                    screen.blit(temp_card, (SCREENWIDTH - temp_card_width // 3, user_cards_y + i * user_cards_gap))
