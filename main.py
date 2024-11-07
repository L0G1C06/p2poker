from utils import shuffle_deck, create_deck, deal_cards, draw_cards, rank_hand
from methods import GameState
import asyncio

async def play_game(num_players: int = 2) -> None:
    deck = await shuffle_deck(create_deck())
    game_state = GameState(deck=deck, players=[[] for _ in range(num_players)])

    for i in range(num_players):
        game_state.players[i] = await deal_cards(game_state=game_state, num_cards=5)

    for i, player_hand in enumerate(game_state.players):
        print(f"Player {i + 1}'s hand: {', '.join(str(card) for card in player_hand)}")

    for i in range(num_players):
        discard_indices = input(f"Player {i + 1}, enter the indices of the cards to discard (0-4, separated by spaces): ")
        discard_indices = [int(index) for index in discard_indices.split()]
        await draw_cards(game_state=game_state, player_idx=i, discard_indices=discard_indices)

    for i, player_hand in enumerate(game_state.players):
        print(f"Player {i + 1}'s final hand: {', '.join(str(card) for card in player_hand)}")

    hand_ranks = [rank_hand(hand=hand) for hand in game_state.players]
    max_rank = max(hand_ranks)
    winner_idx = hand_ranks.index(max_rank)
    print(f"Player {winner_idx + 1} wins with a {', '.join(str(card) for card in game_state.players[winner_idx])}")

if __name__ == "__main__":
    num_players = 2
    asyncio.run(play_game(num_players=num_players))