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
            game_state.active_players = [True] * num_players

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

        determine_winners(game_state)

        # Hand evaluation
        #active_players = [player for i, player in enumerate(game_state.players) if game_state.active_players[i]]
        #if active_players:
        #    hand_ranks = [rank_hand(player.hand + game_state.community_cards) for player in active_players]
        #    max_rank = max(hand_ranks)
        #    winner_idx = hand_ranks.index(max_rank)
        #    winner = active_players[winner_idx]
        #    winner.chips += game_state.pot
        #    print(f"\n{winner.name} wins with {hand_ranks[winner_idx][2]}.")
        #    print(f"Final chip count of {winner.name}: {winner.chips} chips.")
        #else:
        #    print("All the players have fold. There is no winner for this round.")
        
        # Display the final chip count of all players
        for player in game_state.players:
            print(f"{player.name} has {player.chips} chips remaining.")

if __name__ == "__main__":
    num_players = 3
    asyncio.run(play_game(num_players=num_players, num_rounds=1))