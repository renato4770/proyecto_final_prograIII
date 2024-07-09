from abc import ABC, abstractmethod

class Card(ABC):
    def __init__(self, id: int, name: str, effect):
        self.id = id
        self.name = name
        self.effect = effect

    @abstractmethod
    def apply_effect(self, game, player):
        pass

class UnicornCard(Card):
    def apply_effect(self, game, player):
        self.effect(game, player)

class PandaCard(Card):
    def apply_effect(self, game, player):
        self.effect(game, player)
