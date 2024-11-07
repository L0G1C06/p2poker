from utils import shuffle_deck, create_deck, deal_cards, draw_cards, rank_hand
from methods import GameState
import asyncio

async def play_game(num_players: int) -> None:
    if num_players < 2 or num_players > 4:
        raise ValueError("Number of players must be between 2 and 4.")
    deck = await shuffle_deck(create_deck())
    game_state = GameState(deck=deck, players=[[] for _ in range(num_players)])

    for i in range(num_players):
        game_state.players[i] = await deal_cards(game_state=game_state, num_cards=2)

    community_cards = []
    community_cards += await deal_cards(game_state=game_state, num_cards=3)
    print(f"Flop: {', '.join(str(card) for card in community_cards)}")

    community_cards += await deal_cards(game_state=game_state, num_cards=1)  
    print(f"Turn: {', '.join(str(card) for card in community_cards)}")
    
    community_cards += await deal_cards(game_state=game_state, num_cards=1)  
    print(f"River: {', '.join(str(card) for card in community_cards)}")

    for i, player_hand in enumerate(game_state.players):
        print(f"Player {i + 1}'s hand: {', '.join(str(card) for card in player_hand)}")

    hand_ranks = [rank_hand(hand=player_hand + community_cards) for player_hand in game_state.players]
    max_rank = max(hand_ranks)
    winner_idx = hand_ranks.index(max_rank)
    for i, (rank, _, description) in enumerate(hand_ranks):
        print(f"Player {i + 1} has a {description}")
    print(f"\nPlayer {winner_idx + 1} wins with a {hand_ranks[winner_idx][2]}")

if __name__ == "__main__":
    num_players = 2
    asyncio.run(play_game(num_players=num_players))