from typing import List, Dict

from player import Player

class GameState:
    def get_state(self, players: List['Player'], current_player_index: int) -> Dict:
        return {
            'players': [self._get_player_state(player) for player in players],
            'current_player': players[current_player_index].id
        }

    def _get_player_state(self, player: 'Player') -> Dict:
        return {
            'id': player.id,
            'hand_size': len(player.hand),
            'stable': [card.to_dict() for card in player.stable]
        }