import random

def evaluate_hand(hand):
    values = [card.value for card in hand]
    suits = [card.suit for card in hand]
    count = {v: values.count(v) for v in values}
    ordened_values = sorted([v for v in count.keys()], key=lambda x: ('2345678910JQKA'.index(x)), reverse=True)

    def is_flush():
        return len(set(suits)) == 1
    
    def is_straight():
        idx = [Deck.values.index(v) for v in ordened_values]
        return sorted(idx) == list(range(min(idx), min(idx) + 5))
    
    if is_flush() and is_straight():
        if ordened_values == ['A', 'K', 'Q', 'J', '10']:
            return "Royal Flush"
        return "Straight Flush"
    elif 4 in count.values():
        return "Quadra"
    elif 3 in count.values() and 2 in count.values():
        return "Full House"
    elif is_flush():
        return "Flush"
    elif is_straight():
        return "Sequência"
    elif 3 in count.values():
        return "Trinca"
    elif list(count.values()).count(2) == 2:
        return "Dois Pares"
    elif 2 in count.values():
        return "Par"
    else:
        return "Carta Alta"
    
def winner(players):
    classification = ["Carta Alta", "Par", "Dois Pares", "Trinca", "Sequência", "Flush", "Full House", "Quadra", "Straight Flush", "Royal Flush"]

    best_hands = []
    for player in players:
        hand_type = evaluate_hand(player.hand)
        idx = classification.index(hand_type)
        best_hands.append((idx, player.name, hand_type))

    win = max(best_hands, key=lambda x: x[0])
    return win[1], win[2]

class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
    
    def __repr__(self):
        return f"{self.value} of {self.suit}"
    
class Player:
    def __init__(self, name, chips=1000):
        self.name = name
        self.hand = []
        self.chips = chips
        self.current_bet = 0

    def receive_card(self, cards):
        self.hand.append(cards)
    
    def show_hand(self):
        return f"{self.name}: {', '.join(map(str, self.hand))}"
    
    def place_bet(self, amount):
        if amount > self.chips:
            raise ValueError(f"{self.name} doesn't have enough chips!")
        self.chips -= amount
        self.current_bet += amount
        return amount
    
    def reset_bet(self):
        self.current_bet = 0

class Deck:
    values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    suits = ['Hearts', 'Diamonds', 'Spades', 'Clubs']
    
    def __init__(self):
        self.cards = [Card(value=value, suit=suit) for value in self.values for suit in self.suits]
        random.shuffle(self.cards)
    
    def dealing_cards(self):
        return self.cards.pop()

class PokerGame:
    def __init__(self, players, big_blind=10, small_blind=5):
        self.players = players
        self.deck = Deck()
        self.pot = 0
        self.big_blind = big_blind
        self.small_blind = small_blind
        self.current_bet = 0

    def start_round(self):
        # Distribuir duas cartas para cada jogador
        for player in self.players:
            player.receive_card(self.deck.dealing_cards())
            player.receive_card(self.deck.dealing_cards())
        self.pot = 0
        self.current_bet = 0
        self.collect_blinds()
    
    def collect_blinds(self):
        # Assumindo que o primeiro jogador é o small blind e o segundo é o big blind
        self.players[0].place_bet(self.small_blind)
        self.players[1].place_bet(self.big_blind)
        self.pot += self.small_blind + self.big_blind
        self.current_bet = self.big_blind

    def betting_round(self):
        for player in self.players:
            action = input(f"{player.name}, você deseja 'call', 'raise', ou 'fold'? ")
            if action == "call":
                self.call(player)
            elif action == "raise":
                amount = int(input(f"{player.name}, quanto deseja aumentar? "))
                self.raise_bet(player, amount)
            elif action == "fold":
                self.players.remove(player)
    
    def call(self, player):
        to_call = self.current_bet - player.current_bet
        self.pot += player.place_bet(to_call)
    
    def raise_bet(self, player, amount):
        if amount < self.current_bet:
            raise ValueError("O aumento deve ser maior que a aposta atual!")
        self.pot += player.place_bet(amount)
        self.current_bet = amount
    
    def show_pot(self):
        print(f"Pot: {self.pot} fichas")
    
    def determine_winner(self):
        # Aqui você poderia utilizar a função winner() que você já criou
        winner_name, hand_type = winner(self.players)
        print(f"{winner_name} ganha com uma mão de {hand_type}")
        return winner_name, hand_type

    def end_round(self):
        # Determinar o vencedor e entregar o pote
        winner_name = self.determine_winner()
        for player in self.players:
            if player.name == winner_name:
                player.chips += self.pot
        self.pot = 0
        for player in self.players:
            player.reset_bet()