# Alex Scott
# Durak War Games
# Player Class

class Player(object):
	def __init__(self, name):
		self.name = name
		self.uberSuit = ""
		self.hand = []
		self.uberCount = 0
		self.debug = True
		self.endgame = False

		if self.debug == True:
			print("created " + self.name)

# Simple Functions ------------------------------------------------

	def size(self):
		return len(self.hand)

	def isEmpty(self):
		return len(self.hand) == 0

	def pop(self):
		return self.hand.pop()

	def beginEndGame(self):
		self.endgame = True

	def drawCards(self, deck, count):
		"""Required: game must have started
		   pop count cards from deck """
		for n in range(0, count):
			if(deck.size() != 0):
				draw = deck.pop()
				if draw.suit == self.uberSuit: self.uberCount += 1
				self.hand.append(draw)

	def showAll(self):
		for c in self.hand:
			c.showChoice(self.uberSuit)

	def show(self):
		for c in self.hand:
			c.show()

# Player Funcitons ------------------------------------------------
	def getAttackable(self, tablePlayed, defencePlayed):
		playableIndex = list()
		for i, c in enumerate(self.hand, start = 1):
			for played in tablePlayed + defencePlayed:
				if c.sameRank(played): 
					playableIndex.append(i)
		return playableIndex

	def getBounceable(self, tablePlayed):
		bounceableIndex = list()
		if len(tablePlayed) == 1:
			# find bouncableIndex from hand
			for i, c in enumerate(self.hand, start = 1):
				if c.sameRank(tablePlayed[0]):
					bounceableIndex.append(i)
			return bounceableIndex
		else:
			# check if attacked cards are sameRank
			temp = tablePlayed[0]
			for tp in tablePlayed:
				if not tp.sameRank(temp): return bounceableIndex
			# find bounceableIndex from hand
			for i, c in enumerate(self.hand, start = 1):
				if c.sameRank(temp): bounceableIndex.append(i)
			return bounceableIndex

	def getDefendable(self, tablePlayed):
		playableIndex = list()
		highestUber = None

		for tp in tablePlayed:
			if tp != None and tp.suit == self.uberSuit:
				if highestUber == None: highestUber = tp
				elif tp.isGreater(highestUber): highestUber = tp

		for i, c in enumerate(self.hand, start = 1):
			found = False
			for tp in tablePlayed:
				if tp != None and tp.suit != self.uberSuit and c.sameSuit(tp) and c.isGreater(tp):
					c.showChoice(self.uberSuit)
					found = True
					playableIndex.append(i)
			if c.suit == self.uberSuit:
				if highestUber == None:
					c.showChoice(self.uberSuit)
					found = True
					playableIndex.append(i)
				elif c.isGreater(highestUber):
					c.showChoice(self.uberSuit)
					found = True
					playableIndex.append(i)

			elif found == False:
				c.show()

		return playableIndex

	def canAttack(self, tablePlayed, defencePlayed):
		for c in self.hand:
			for tableCard in tablePlayed + defencePlayed:
				if c.sameRank(tableCard): return True 
		return False

	def sortHand(self):
		nonUber = list()
		Uber = list()
		for c in self.hand:
			if c.suit != self.uberSuit: nonUber.append(c)
			else: Uber.append(c)

		self.hand = []
		nonUber.sort(key=lambda c: c.rank)
		Uber.sort(key=lambda c: c.rank)
		self.hand.extend(nonUber)
		self.hand.extend(Uber)