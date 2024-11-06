#from methods import *
from rules import *

def start_game():
    # Cria os jogadores e inicia o PokerGame com blinds
    players = [Player("Player1"), Player("Player2")]
    game = PokerGame(players, big_blind=10, small_blind=5)

    # Inicia a rodada: distribui as cartas e aplica as blinds
    game.start_round()

    # Exibe a mão inicial dos jogadores
    for player in players:
        print(player.show_hand())

    # Rodada de apostas (por simplicidade, rodamos uma única vez aqui)
    game.betting_round()
    game.show_pot()  # Mostra o pote atual

    # Avaliação das mãos e determinação do vencedor
    game.determine_winner()

    # Exibe o saldo de fichas dos jogadores após a rodada
    for player in players:
        print(f"{player.name} tem {player.chips} fichas restantes")

if __name__ == "__main__":
    start_game()