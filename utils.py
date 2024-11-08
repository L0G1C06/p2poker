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

async def place_blinds(game_state: GameState):
    small_blind_pos = (game_state.dealer_pos + 1) % len(game_state.players)
    big_blind_pos = (small_blind_pos + 1) % len(game_state.players)

    small_blind_player = game_state.players[small_blind_pos]
    big_blind_player = game_state.players[big_blind_pos]

    game_state.pot += game_state.small_blind
    small_blind_player.bet(game_state.small_blind)

    game_state.pot += game_state.big_blind
    big_blind_player.bet(game_state.big_blind)

    print(f"Player {small_blind_pos + 1} posts the small blind.")
    print(f"Player {big_blind_pos + 1} posts the big blind.\n")
    
    return small_blind_pos, big_blind_pos

async def betting_round(game_state: GameState, is_preflop: bool = False, small_blind_pos: int = None, big_blind_pos: int = None):
    raise_occured = False
    print("\nStarting a new betting round...")

    for i, player in enumerate(game_state.players):
        if not game_state.active_players[i]:
            continue

        if is_preflop and (i == small_blind_pos or i == big_blind_pos):
            continue

        if is_preflop:
            options = ["call", "raise", "fold"]
        else:
            options = ["check", "raise", "fold"] if not raise_occured else ["call", "raise", "fold"]
        
        # Display current player chip count
        print(f"\n{player.name} has {player.chips} chips.")
        print(f"Current pot: {game_state.pot} chips.")
        
        while True:
            action = input(f"{player.name}, choose an action ({'/'.join(options)}): ").strip().lower()
            if action in options:
                break
            else:
                print(f"Invalid action. Please choose a valid option.")

        if action == "fold":
            game_state.active_players[i] = False
            print(f"{player.name} folded.")
        elif action == "raise":
            raise_amount = int(input(f"{player.name}, how much do you want to raise? "))
            if raise_amount > player.chips:
                print("Not enough chips to make this bet.")
                continue
            player.bet(raise_amount)
            game_state.pot += raise_amount
            print(f"{player.name} raised by {raise_amount} chips.")
            raise_occured = True
        elif action == "call":
            call_amount = max(player.current_bet for player in game_state.players) - player.current_bet
            if call_amount > player.chips:
                call_amount = player.chips  # Player can call all-in if they don't have enough chips
            player.bet(call_amount)
            game_state.pot += call_amount
            print(f"{player.name} called with {call_amount} chips.")
        elif action == "check":
            print(f"{player.name} checked.")
        
    print(f"Betting round complete. Final pot: {game_state.pot} chips.\n")

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

def show_player_hand(game_state: GameState):
    print("\nPlayers hand:")
    for player in game_state.players:
        hand_str = ', '.join(str(card) for card in player.hand)
        print(f"{player.name}: {hand_str}")