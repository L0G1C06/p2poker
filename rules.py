from methods import *

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