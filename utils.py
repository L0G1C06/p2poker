import asyncio
import random
from typing import List, Tuple
from collections import Counter
from itertools import combinations

from methods import Card, Suit, Rank, GameState

def create_deck() -> List[Card]:
    return [Card(suit, rank) for suit in Suit for rank in Rank]

async def shuffle_deck(deck: List[Card]) -> List[Card]:
    await asyncio.sleep(0)
    random.shuffle(deck)
    return deck

async def deal_cards(game_state: GameState, num_cards: int) -> List[Card]:
    return [game_state.deck.pop() for _ in range(num_cards)]

async def place_blinds(num_players: int, dealer_pos: int):
    small_blind_pos = (dealer_pos + 1) % num_players
    big_blind_pos = (dealer_pos + 2) % num_players
    print(f"Player {small_blind_pos + 1} posts the small blind.")
    print(f"Player {big_blind_pos + 1} posts the big blind.\n")
    return small_blind_pos, big_blind_pos

async def betting_round(num_players: int, dealer_pos: int, start_pos: int, is_preflop: bool = False, small_blind_pos: int = None, big_blind_pos: int = None) -> None:
    raise_occured = False
    print("\nStarting a new betting round...")
    # Placeholder for betting round logic
    for i in range(num_players):
        player_pos = (start_pos + i) % num_players
        if is_preflop and (player_pos == small_blind_pos or player_pos == big_blind_pos):
            continue

        if is_preflop:
            options = ["call", "raise", "fold"]
        else:
            options = ["check", "raise", "fold"] if not raise_occured else ["call", "raise", "fold"]

        action = input(f"Player {player_pos + 1}, choose an action ({'/'.join(options)}): ").strip().lower()
        if action == "fold":
            print(f"Player {player_pos + 1} folds.")
        elif action == "raise":
            print(f"Player {player_pos + 1} raises.")
            raise_occured = True
        elif action == "call":
            print(f"Player {player_pos + 1} calls.")
        elif action == "check":
            print(f"Player {player_pos + 1} checks.")
        else:
            print(f"Invalid action by Player {player_pos + 1}.")
    print("Betting round complete.\n")

def evaluate_five_card_hand(hand: List[Card]) -> Tuple[int, List[int], str]:
    ranks = sorted([card.rank.value for card in hand], reverse=True)
    suits = [card.suit for card in hand]
    rank_counts = Counter(ranks)
    is_flush = len(set(suits)) == 1
    is_straight = len(set(ranks)) == 5 and max(ranks) - min(ranks) == 4

    if is_straight and is_flush:
        return (8, ranks, "Straight Flush")
    elif 4 in rank_counts.values():
        return (7, ranks, "Four of a Kind")
    elif sorted(rank_counts.values()) == [2, 3]:
        return (6, ranks, "Full House")
    elif is_flush:
        return (5, ranks, "Flush")
    elif is_straight:
        return (4, ranks, "Straight")
    elif 3 in rank_counts.values():
        return (3, ranks, "Three of a Kind")
    elif list(rank_counts.values()).count(2) == 2:
        return (2, ranks, "Two Pair")
    elif 2 in rank_counts.values():
        return (1, ranks, "One Pair")
    else:
        return (0, ranks, "High Card")

def rank_hand(hand: List[Card]) -> Tuple[int, List[int], str]:
    best_rank = (0, [], "")
    for combo in combinations(hand, 5):
        combo_rank = evaluate_five_card_hand(list(combo))
        if combo_rank[0] > best_rank[0] or (combo_rank[0] == best_rank[0] and combo_rank[1] > best_rank[1]):
            best_rank = combo_rank
    return best_rank