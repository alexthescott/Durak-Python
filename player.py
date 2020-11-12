class Player:
    def __init__(self, name, is_user, id):
        self.name = name
        self.is_user = is_user
        self.id = id
        self.hand = []
        self.uber_count = 0

    def __len__(self):
        return len(self.hand)

    def __str__(self):
        return str(self.name) + "\n" + "".join([str(c) + "\n" for c in self.hand])[:-1]

    def get_lowest_card(self):
        # hand must be sorted
        return self.hand[0]

    def draw_card(self, card):
        self.hand.append(card)

    def need_more_cards(self):
        return len(self) < 6

    def sort_hand(self):
        non_uber_cards = [c for c in self.hand if c.uber is not c.suit]
        non_uber_cards.sort(key=lambda c: c.rank)

        uber_cards = [c for c in self.hand if c.uber is c.suit]
        uber_cards.sort(key=lambda c: c.rank)

        self.hand = non_uber_cards + uber_cards


