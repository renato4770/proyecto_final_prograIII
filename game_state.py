from typing import List, Dict

class GameState:
        def __init__(self):
            self.players = []
            self.current_player = None

        def update_state(self, state):
            self.players = state['players']
            self.current_player = state['current_player']

        def get_state(self, player_id):
            return {
                'players': self.players,
                'current_player': self.current_player,
                'player_id': player_id
            }