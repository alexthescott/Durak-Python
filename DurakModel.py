#!/usr/bin/env python3
""" Inspired in part by https://github.com/k41n/durak-python
Alex Scott
alphaDurak 
Summer 2019

RULES:
	The goal is to not be the last person with cards
	remainingPlayers attack and defend until no cards
	in the deck remain, at which point players attack
	until one player remains. 

	Attack the 'left' player, defend with a higher card 
	with the same suit. Uber cards beat all other suits
	All non-defenders can contribute cards of the same 
	value as cards played in the phase, adding to the
	defence responsibility.

	Can forfeit an attack at any time, at the cost of 
	forgoing the defender's next attack. Can only attack
	with the size of the defender's hand.

	At the end of a phase, players with fewer than 6 
	cards pick up until they have 6 cards. 

	Can bounce the attack by playing a same value card,  
	pushing the card to the 'left' or the 'right' passing 
	defence responsibility. This will be a successful 
	defence for the initial defender

	Can replace the placeholder uber with an uber with a 
	value of 2, which then becomes the last card of the 
	deck

	Last player remaining is the fool
"""
import random
import time
from card import Card
from player import Player
from deck import Deck
from simpleAgent import SimpleAgent
from stupidAgent import StupidAgent

class Game:
	""" Creates game instance with a Deck, Players
		Durak phases are played until there is a loser
	""" 
	def __init__(self):
		self.deck = Deck()
		self.players = list()
		self.tablePlayed = list()
		self.defencePlayed = list()
		self.inPhase = False
		self.activeAttacker = 0
		self.playerCount = 0
		self.uberSuit = ""
		self.bounceIndex = 0
		self.topCard = None
		self.debug = True

		if self.debug == True:
			print("created Game")

	def getPlayers(self): return self.players
	def getPlayer(self, name): 
		for p in self.players:
			if p.name == name:
				return p
		return None
	def getDeck(self): return self.deck
	def getDeckSize(self): return self.deck.size()
	def getUberSuit(self): return uberSuit
	def getTopCard(self): return self.topCard
	def getPlayerCount(self): return self.playerCount
	def getAttacker(self): return self.players[self.activeAttacker % self.playerCount]
	def getAttackerIndex(self): return self.activeAttacker
	def getDefenderIndex(self): return (self.activeAttacker + 1 + self.bounceIndex) % self.playerCount
	def getDefender(self):
		defenderIndex = self.activeAttacker + self.bounceIndex
		return self.players[defenderIndex % self.playerCount]

	def addPlayer(self, player):
		self.players.append(player)
		self.playerCount += 1

		if self.debug == True:
			print("added " + player.name)

	def start(self):
		self.deck = Deck()
		self.deck.shuffle()

		self.topCard = self.deck.pop()
		self.deck.cards.insert(0, self.topCard)
		self.uberSuit = self.topCard.suit

		if self.debug == True:
			playerNames = ""
		
		for p in self.players:
			p.uberSuit = self.uberSuit

			if self.debug == True:
				playerNames = playerNames + p.name + " "

		self.deal()
		self.sortPlayersHand()

		if self.debug == True:
			print("started Durak with " + playerNames)

	def nextPhase(self):
		self.inPhase = True

		if self.deck.size() == 0:
			for p in self.players:
				if p.isEmpty(): self.players.remove(p)

		self.deal()
		self.sortPlayersHand()
		self.tablePlayed.clear()
		self.defencePlayed.clear()

		if self.playerCount <= 1:
			return False

		outcome = self.phase()
		# 1 if successful defence
		# 0 if failed defence
		if outcome == 1:
			self.nextPlayerIndex()
		elif outcome == 0:
			defenderIndex = self.getDefenderIndex()
			self.takeTablePlayed(self.players[defenderIndex])
			self.nextPlayerIndex()
			self.nextPlayerIndex()

		self.inPhase = False
	def nextPlayerIndex(self):
		if self.activeAttacker == len(self.players): 
			self.activeAttacker = 0
		else: 
			self.activeAttacker += 1

	def phase(self):
		# return 1 if successful defence
		# return 0 if failed defence
		if self.debug == True:
			print("new phase " + self.getAttacker().name + " is attacking")

		self.bounceIndex = 0
		while True:
			if len(self.tablePlayed) == 0:
				self.lastAttack = self.attack(self.players[self.activeAttacker - 1])
				if self.lastAttack != None: 
					self.tablePlayed.append(self.lastAttack)

			if not self.canDefend():
				return 0 

			if self.lastAttack == None and len(self.tablePlayed) == len(self.defencePlayed):
				return 1

			time.sleep(3)

			self.lastDefence = self.defend()
			if self.lastDefence == None:
				return 0

			if not self.canContribute():
				return 1

			time.sleep(3)

			contributerIndex = self.getContributersIndex()
			for i in contributerIndex:
				self.lastAttack = self.attack(self.players[i])
				if self.lastAttack != None:
					break

	def defend(self):
		defender = self.getDefender()
		defence = defender.startDefence(self.tablePlayed)
		if defence == None: return None
		else:
			return defence
			defender.hand.remove(defence)
	def attack(self, player):
		attack = player.startAttack(self.tablePlayed, self.defencePlayed)
		if attack == None: return None
		else:
			return attack

	def takeTablePlayed(self, player):
		player.hand.extend(self.tablePlayed)
		player.hand.extend(self.defencePlayed)
		self.tablePlayed = list()
		self.defencePlayed = list()
	def deal(self):
		for p in self.players:
			if p.size() < 6: p.drawCards(self.deck, 6 - p.size())
	def sortPlayersHand(self):
		for p in self.players: 
			p.sortHand()

	def canDefend(self):
		defender = self.getDefender()
		availableDefence = []
		availableDefence.extend(defender.hand)

		highestUber = None
		coverable = 0
		
		# Count highest uber attack
		for tp in self.tablePlayed:
			if tp != None and tp.suit == self.uberSuit:
				if highestUber == None: highestUber = tp
				elif tp.isGreater(highestUber): highestUber = tp

		for c in availableDefence:
			if c.suit == self.uberSuit:
				if highestUber == None or c.isGreater(highestUber):
					availableDefence.remove(c)
					coverable += 1
	
		for tp in self.tablePlayed:
			for h in availableDefence:
				if tp != None and h.sameSuit(tp) and h.isGreater(tp): 
					availableDefence.remove(h)
					coverable += 1
					break
		return coverable >= len(self.tablePlayed)
	def canContribute(self):
		if len(self.tablePlayed) == 0: 
			return True
		else:
			tempContributors = (self.players[1 - self.activeAttacker:] + self.players[:1 - self.activeAttacker])
			for p in tempContributors:
				for c in p.hand:
					for t in self.tablePlayed + self.defencePlayed:
						if c.sameRank(t):
							return True
		return False

	def getContributersIndex(self):
		tempContributors = list()
		for i, p in enumerate(tempContributors):
			for c in p.hand:
				for t in self.tablePlayed + self.defencePlayed:
					if c.sameRank(t):
						tempContributors.append(i)
		return tempContributors

	def finished(self):
		# return boolean if finished
		if not self.deck.isEmpty():
			return False
		activeAttackersLeft = 0
		for p in self.players:
			if p.isEmpty() == False: activeAttackersLeft += 1
			if activeAttackersLeft > 1: 
				self.playerCount = activeAttackersLeft
				return False
		return True
