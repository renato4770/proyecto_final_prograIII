from abc import ABC, abstractmethod

class Card(ABC):
    def __init__(self, id: int, name: str, effect):
        self.id = id
        self.name = name
        self.effect = effect

    def to_dict(self):
        return {"id": self.id, "name": self.name}    

    @abstractmethod
    def apply_effect(self, game, player):
        pass

class UnicornCard(Card):
    def __init__(self, id: int, name: str, effect):
        super().__init__(id, name, effect)

    def apply_effect(self, game, player):
        self.effect(game, player)

class BabyUnicornCard(Card):
    def __init__(self, id: int, name: str):
        super().__init__(id, name, None)  # Baby Unicorns typically don't have an effect

    def apply_effect(self, game, player):
        pass  # Baby Unicorns typically don't have an effect        

class PandaCard(Card):
    def __init__(self, id: int, name: str, effect):
        super().__init__(id, name, effect)

    def apply_effect(self, game, player):
        self.effect(game, player)
