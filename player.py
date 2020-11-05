class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.uber_count = 0

    def __len__(self):
        return len(self.hand)

    def draw_card(self):
        self.hand.append()

    def sort_hand(self):
        print('to_do, sort hand')