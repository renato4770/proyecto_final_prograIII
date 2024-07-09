class Player:
    def __init__(self, player_id: str):
        self.id = player_id
        self.hand = []
        self.stable = []

    def draw_card(self, card):
        self.hand.append(card)

    def get_card(self, card_index: int):
        if card_index < len(self.hand):
            return self.hand[card_index]
        return None

    def play_card(self, card):
        self.hand.remove(card)
        self.stable.append(card)
