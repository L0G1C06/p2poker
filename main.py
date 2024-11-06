from methods import *
from rules import *

def start_game():
    deck = Deck()
    players = [Player("Player1"), Player("Player2")]

    for _ in range(5):
        for player in players:
            player.receive_card(deck.dealing_cards())

    for player in players:
        print(player.show_hand())
        print(f"Combinação: {evaluate_hand(player.hand)}")

    player_winner, hand_type = winner(players)
    print(f"\nO vencedor é {player_winner} com a mão: {hand_type}")

if __name__ == "__main__":
    start_game()