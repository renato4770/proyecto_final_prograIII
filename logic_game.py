from card import UnicornCard, PandaCard
from player import Player
from deck import Deck, DeckBuilder
from typing import List

class LogicGame:
    def __init__(self):
        self.players: List[Player] = []
        self.current_player_index: int = 0
        deck_builder = DeckBuilder()
        deck_builder.add_unicorn_cards(20)
        deck_builder.add_panda_cards(10)
        deck_builder.shuffle()
        self.deck: Deck = deck_builder.build()

    def add_player(self, player_id: str) -> Player:
        player = Player(player_id)
        self.players.append(player)
        self.deal_initial_hand(player)
        return player

    def deal_initial_hand(self, player: Player):
        for _ in range(5):
            card = self.deck.draw_card()
            if card:
                player.draw_card(card)

    def play_card(self, player_id: str, card_id: int):
        player = self.get_player(player_id)
        if player == self.players[self.current_player_index]:
            card = player.get_card(card_id)
            if card:
                card.apply_effect(self, player)
                player.play_card(card)

    def draw_card(self, player_id: str):
        player = self.get_player(player_id)
        if player == self.players[self.current_player_index]:
            player.draw_card(self.deck.draw_card())

    def end_turn(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def get_player(self, player_id: str) -> Player:
        return next(player for player in self.players if player.id == player_id)

    def get_game_state(self):
        return {
            "players": [
                {
                    "id": player.id,
                    "hand": [{"id": card.id, "name": card.name} for card in player.hand],
                    "stable": [{"id": card.id, "name": card.name} for card in player.stable]
                } for player in self.players
            ],
            "current_player": self.players[self.current_player_index].id
        }
