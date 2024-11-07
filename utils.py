import asyncio
import random
from typing import List, Tuple
from collections import Counter

from methods import Card, Suit, Rank, GameState

def create_deck() -> List[Card]:
    return [Card(suit, rank) for suit in Suit for rank in Rank]

async def shuffle_deck(deck: List[Card]) -> List[Card]:
    await asyncio.sleep(0)
    random.shuffle(deck)
    return deck

async def deal_cards(game_state: GameState, num_cards: int) -> List[Card]:
    new_cards = []
    for _ in range(num_cards):
        card = game_state.deck.pop()
        new_cards.append(card)
    return new_cards

def rank_hand(hand: List[Card]) -> Tuple[int, List[int]]:
    ranks = sorted([card.rank.value for card in hand], reverse=True)
    suits = [card.suit for card in hand]
    rank_counts = Counter(ranks)
    is_flush = len(set(suits)) == 1
    is_straight = len(set(ranks)) == 5 and max(ranks) - min(ranks) == 4
    if is_straight and is_flush:
        return (8, ranks)  # Straight flush
    elif 4 in rank_counts.values():
        return (7, ranks)  # Four of a kind
    elif sorted(rank_counts.values()) == [2, 3]:
        return (6, ranks)  # Full house
    elif is_flush:
        return (5, ranks)  # Flush
    elif is_straight:
        return (4, ranks)  # Straight
    elif 3 in rank_counts.values():
        return (3, ranks)  # Three of a kind
    elif list(rank_counts.values()).count(2) == 2:
        return (2, ranks)  # Two pairs
    elif 2 in rank_counts.values():
        return (1, ranks)  # One pair
    else:
        return (0, ranks) 

async def draw_cards(game_state: GameState, player_idx: int, discard_indices: List[int]) -> None:
    player_hand = game_state.players[player_idx]
    for index in sorted(discard_indices, reverse=True):
        del player_hand[index]
    new_cards = await deal_cards(game_state, len(discard_indices))
    game_state.players[player_idx] = player_hand + new_cards