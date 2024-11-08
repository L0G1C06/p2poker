from utils import *
from methods import GameState
import asyncio

async def play_game(num_players: int, num_rounds: int, starting_chips: int = 1000) -> None:
    deck = await shuffle_deck(create_deck())
    game_state = GameState(deck=deck, num_players=num_players, starting_chips=starting_chips)
    
    for round_num in range(num_rounds):
        print(f"\n-- Round {round_num + 1} --")
        
        # Reset the game state at the beginning of each round
        game_state.reset_round()

        # Place blinds
        small_blind_pos, big_blind_pos = await place_blinds(game_state=game_state)

        # Deal cards
        for player in game_state.players:
            player.hand = await deal_cards(game_state, num_cards=2)
            player.current_bet = 0  # Reset player's bet at the start of the round

        show_player_hand(game_state=game_state)
        
        # Pre-flop betting
        await betting_round(game_state, is_preflop=True, small_blind_pos=small_blind_pos, big_blind_pos=big_blind_pos)

        # Flop
        game_state.community_cards = await deal_cards(game_state, num_cards=3)
        print(f"Flop: {', '.join(str(card) for card in game_state.community_cards)}")
        await betting_round(game_state)

        # Turn
        game_state.community_cards += await deal_cards(game_state, num_cards=1)
        print(f"Turn: {', '.join(str(card) for card in game_state.community_cards)}")
        await betting_round(game_state)

        # River
        game_state.community_cards += await deal_cards(game_state, num_cards=1)
        print(f"River: {', '.join(str(card) for card in game_state.community_cards)}")
        await betting_round(game_state)

        # Hand evaluation
        hand_ranks = [rank_hand(player.hand + game_state.community_cards) for player in game_state.players]
        max_rank = max(hand_ranks)
        winner_idx = hand_ranks.index(max_rank)
        print(f"\n{game_state.players[winner_idx].name} wins with {hand_ranks[winner_idx][2]}.")
        print(f"Final chip count of {game_state.players[winner_idx].name}: {game_state.players[winner_idx].chips} chips.")
        
        # Display the final chip count of all players
        for player in game_state.players:
            print(f"{player.name} has {player.chips} chips remaining.")

if __name__ == "__main__":
    num_players = 3
    asyncio.run(play_game(num_players=num_players, num_rounds=1))