import random
from card import UnicornCard, PandaCard
from card_effects import unicorn_effect, panda_effect

class Deck:
    def __init__(self, cards):
        self.cards = cards

    def draw_card(self):
        return self.cards.pop(0) if self.cards else None

class DeckBuilder:
    def __init__(self):
        self.cards = []

    def add_unicorn_cards(self, count):
        for i in range(count):
            self.cards.append(UnicornCard(i, f"Unicorn {i+1}", unicorn_effect))

    def add_panda_cards(self, count):
        for i in range(count):
            self.cards.append(PandaCard(i + 20, f"Panda {i+1}", panda_effect))

    def shuffle(self):
        random.shuffle(self.cards)

    def build(self):
        return Deck(self.cards)
