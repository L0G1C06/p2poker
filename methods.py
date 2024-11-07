from dataclasses import dataclass
from enum import Enum
from typing import List

class Suit(Enum):
    SPADES = "♠"
    HEARTS = "♥"
    DIAMONDS = "♦"
    CLUBS = "♣"

class Rank(Enum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14

class Player:
    def __init__(self, name: str, chips: int):
        self.name = name
        self.chips = chips
        self.hand: List[Card] = []
        self.current_bet = 0

    def bet(self, amount: int):
        if amount > self.chips:
            raise ValueError(f"Player {self.name} doesn't have enough chips to bet {amount}")
        self.chips -= amount
        self.current_bet += amount
        return amount
    
    def reset_bet(self):
        self.current_bet = 0

@dataclass
class Card:
    suit: Suit
    rank: Rank

    def __str__(self):
        return f"{self.rank.name.capitalize()}{self.suit.value}"

@dataclass
class GameState:
    def __init__(self, deck: List[Card], num_players: int, starting_chips: int, small_blind: int = 1, big_blind: int = 2):
        self.deck = deck
        self.players = [Player(f"Player {i+1}", starting_chips) for i in range(num_players)]
        self.community_cards: List[Card] = []
        self.pot = 0
        self.dealer_pos = 0  # Track dealer position for blinds rotation
        self.active_players = [True] * num_players  # Track active players during the round
        self.small_blind = small_blind
        self.big_blind = big_blind

    def reset_round(self):
        self.community_cards = []
        self.pot = 0
        for player in self.players:
            player.reset_bet()