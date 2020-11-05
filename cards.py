from random import shuffle


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.uber = False

    def __str__(self):
        return "{} of {}".format(self.rank, self.suit)

    def __gt__(self, other):
        # self > other
        # Needs to be tested
        if self.uber and other.uber:
            return self.rank > other.rank
        elif self.uber and not other.uber:
            return True
        elif not self.uber and other.uber:
            return False
        elif self.suit == other.suit:
            return self.rank > other.rank
        else:
            print("Incorrectly comparing two cards")
            return None


class Deck:
    def __init__(self):
        self.suits = ['Spades', 'Hearts', 'Diamonds', 'Clubs']
        self.ranks = list(range(2, 15))
        self.cards_list = []
        self.build()

    def build(self):
        for s in self.suits:
            for r in self.ranks:
                self.cards_list.append(Card(r, s))

    def shuffle(self):
        shuffle(self.cards)

    def __len__(self):
        return len(self.cards_list)

    def __str__(self):
        return "Deck has {} cards left".format(len(self.cards_list))

