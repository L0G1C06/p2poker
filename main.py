from utils import *
from methods import GameState
import asyncio

async def play_game(num_players: int, num_rounds: int) -> None:
    if num_players < 2 or num_players > 4:
        raise ValueError("Number of players must be between 2 and 4.")
    
    deck = await shuffle_deck(create_deck())
    game_state = GameState(deck=deck, players=[[] for _ in range(num_players)], community_cards = [])
    
    game_state.dealer_pos = 0
    
    for round_num in range(num_rounds):
        print(f"\n-- Rodada {round_num + 1} --")

        # move a posição do dealer a cada rodada
        game_state.dealer_pos = (game_state.dealer_pos + 1) % num_players

        community_cards = []

        # apostar blinds
        small_blind, big_blind = await place_blinds(num_players=num_players, dealer_pos=game_state.dealer_pos)

        for i in range(num_players):
            game_state.players[i] = await deal_cards(game_state=game_state, num_cards=2)

        # Pré flop, small and big blind
        active_players = await betting_round(num_players=num_players, dealer_pos=game_state.dealer_pos, start_pos=(big_blind + 1) % num_players, is_preflop=True, big_blind_pos=big_blind, small_blind_pos=small_blind)

        # next players, can choose only call, raise or fold

        for i, player_hand in enumerate(game_state.players):
            if active_players[i]:
                print(f"Player {i + 1}'s hand: {', '.join(str(card) for card in player_hand)}")

        community_cards += await deal_cards(game_state=game_state, num_cards=3)
        print(f"Flop: {', '.join(str(card) for card in community_cards)}")
        active_players = await betting_round(num_players, game_state.dealer_pos, start_pos=small_blind, active_players=active_players)

        # a partir do flop até o River, se não houver nenhuma raise, só pode aparecer como opção check, raise ou fold

        community_cards += await deal_cards(game_state=game_state, num_cards=1)  
        print(f"Turn: {', '.join(str(card) for card in community_cards)}")
        active_players = await betting_round(num_players, game_state.dealer_pos, start_pos=small_blind, active_players=active_players)

        community_cards += await deal_cards(game_state=game_state, num_cards=1)  
        print(f"River: {', '.join(str(card) for card in community_cards)}")
        active_players = await betting_round(num_players, game_state.dealer_pos, start_pos=small_blind, active_players=active_players)

        hand_ranks = [rank_hand(hand=player_hand + community_cards) for player_hand in game_state.players]
        max_rank = max(hand_ranks)
        winner_idx = hand_ranks.index(max_rank)
        for i, (rank, _, description) in enumerate(hand_ranks):
            print(f"Player {i + 1} has a {description}")
        print(f"\nPlayer {winner_idx + 1} wins with a {hand_ranks[winner_idx][2]}")

if __name__ == "__main__":
    num_players = 3
    asyncio.run(play_game(num_players=num_players, num_rounds=2))