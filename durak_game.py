import pygame
from math import ceil

# local imports
from cards import Deck, Card
from constants import *
from player import Player


class Durak:
    def __init__(self, pygame_clock):
        self.pygame_clock = pygame_clock
        self.gameDeck = Deck()
        self.deckImages = {}
        self.load_image_assets()
        self.debugPrint = True

        self.dt = 0
        self.back_card = self.deckImages.get("back")

        self.did_deal_cards_init = False

        """
        self.back_card_image = self.back_card
        self.back_card_rect = self.back_card_image.get_rect()
        self.back_card_rect.x, self.back_card_rect.y = (SCREENWIDTH // 2), (SCREENHEIGHT // 2) - (self.back_card.get_rect().size[1] // 2)
        self.angle = 0
        """
        self.currently_animating_deck = True
        self.currently_animating_deal = True

        # used in self.animate_init_deck
        self.animate_deck_cards_count = 1

        self.players = []

        self.add_player(Player("Alex", True))
        self.add_player(Player("Bot", False))

    def update(self):
        if not self.did_deal_cards_init and not self.currently_animating_deck:
            self.deal_cards_init()
            self.did_deal_cards_init = True

    def draw_deck(self, screen):
        deck_print_size = round(len(self.gameDeck)//1.5)
        cardWidth, cardHeight = self.back_card.get_rect().size
        deckX = (SCREENWIDTH // 2)
        deckY = (SCREENHEIGHT // 2) - (cardHeight // 2)

        for i in range(ceil(deck_print_size / 3)):
            screen.blit(self.back_card, (deckX + 5 + i * 2, deckY + i * 2))

        # self.screen.blit(topCard, (deckX - cardWidth - 5, deckY))

    def animate_init_deck(self, screen):
        cardWidth, cardHeight = self.back_card.get_rect().size
        deckX = (SCREENWIDTH // 2)
        deckY = (SCREENHEIGHT // 2) - (cardHeight // 2)
        for i in range(9):
            if i == self.animate_deck_cards_count // 3:
                self.animate_deck_cards_count += 1
                return True
            screen.blit(self.back_card, (deckX + 5 + i * 2, deckY + i * 2))
        # we've animated it all
        self.animate_deck_cards_count = 1
        return False

    def render(self, screen):
        self.dt = self.pygame_clock.tick(60) / 1000.0
        if self.currently_animating_deck:
            self.currently_animating_deck = self.animate_init_deck(screen)
        else:
            self.draw_deck(screen)
            self.draw_players(screen)

    def add_player(self, player):
        self.players.append(player)

    def deal_cards_init(self):
        # deal card by card
        for i in range(6):
            for p in self.players:
                if p.need_more_cards():
                    p.draw_card(self.gameDeck.pop())
                    p.sort_hand()

    def draw_players(self, screen):
        for p in self.players:
            if p.is_user:
                user_cards_x = SCREENWIDTH // 4
                user_cards_x_end = SCREENWIDTH - SCREENWIDTH // 4
                user_cards_gap = (user_cards_x_end - user_cards_x) / len(p)
                for i, c in enumerate(p.hand):
                    # temp_card = self.back_card.copy()
                    temp_card = self.deckImages.get(c.suit + str(c.rank))
                    temp_card_height = temp_card.get_rect().size[1]
                    screen.blit(temp_card, (user_cards_x + i * user_cards_gap, SCREENHEIGHT - temp_card_height // 2))

    def load_image_assets(self):
        self.deckImages.update({"back": pygame.image.load('Res/Cards/BackCard.png').convert_alpha()})
        for s in self.gameDeck.suits:
            for r in self.gameDeck.ranks:
                card_name = s + str(r)
                card_path = "Res/Cards/" + card_name + ".png"
                self.deckImages.update({card_name: pygame.image.load(card_path).convert_alpha()})

    """
    def animate_deck(self, screen):
        self.back_card_image = pygame.transform.rotate(self.back_card, self.angle)
        self.angle += 2
        x, y = self.back_card_rect.center
        self.back_card_rect = self.back_card_image.get_rect()
        self.back_card_rect.center = (x, y)
        return self.angle != 180
    """