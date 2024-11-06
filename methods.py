import random
from rules import *

class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
    
    def __repr__(self):
        return f"{self.value} of {self.suit}"
    
class Player:
    def __init__(self, name, chips=1000):
        self.name = name
        self.hand = []
        self.chips = chips
        self.current_bet = 0

    def receive_card(self, cards):
        self.hand.append(cards)
    
    def show_hand(self):
        return f"{self.name}: {', '.join(map(str, self.hand))}"
    
    def place_bet(self, amount):
        if amount > self.chips:
            raise ValueError(f"{self.name} doesn't have enough chips!")
        self.chips -= amount
        self.current_bet += amount
        return amount
    
    def reset_bet(self):
        self.current_bet = 0