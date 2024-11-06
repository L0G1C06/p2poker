import random

class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
    
    def __repr__(self):
        return f"{self.value} of {self.suit}"
    
class Deck:
    values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    suits = ['Hearts', 'Diamonds', 'Spades', 'Clubs']
    
    def __init__(self):
        self.cards = [Card(value=value, suit=suit) for value in self.values for suit in self.suits]
        random.shuffle(self.cards)
    
    def dealing_cards(self):
        return self.cards.pop()
    
class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def receive_card(self, cards):
        self.hand.append(cards)
    
    def show_hand(self):
        return f"{self.name}: {', '.join(map(str, self.hand))}"