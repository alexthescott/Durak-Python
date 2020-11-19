from player import Player

class simpleBot(Player):
    def __init__(self, name, id):
        Player.__init__(self, name, False, id)