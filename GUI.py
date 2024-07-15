import tkinter as tk
from logic_game import LogicGame
from client import Client

class GUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Unstable Unicorns")
        self.game = LogicGame()
        self.player_frames = []
        self.hand_buttons = []
        self.client = Client('127.0.0.1', 5555, self)
        self.player_id = None
        self.setup_network()
        self.setup_gui()

    def setup_network(self):
        self.client.connect()

    def setup_gui(self):
        main_frame = tk.Frame(self.master)
        main_frame.pack(padx=10, pady=10)

        self.player_frames = []
        for i in range(4):
            player_frame = tk.LabelFrame(main_frame, text=f"Jugador {i+1}")
            player_frame.grid(row=i//2, column=i%2, padx=5, pady=5)
            self.player_frames.append(player_frame)

            stable_label = tk.Label(player_frame, text="Establo:")
            stable_label.pack()
            stable_listbox = tk.Listbox(player_frame, height=5)
            stable_listbox.pack()

        hand_frame = tk.LabelFrame(main_frame, text="Tu Mano")
        hand_frame.grid(row=2, column=0, columnspan=2, pady=10)

        for i in range(5):
            card_button = tk.Button(hand_frame, text=f"Carta {i+1}", command=lambda i=i: self.client.play_card(i))
            card_button.grid(row=0, column=i, padx=2)
            self.hand_buttons.append(card_button)

        action_frame = tk.Frame(main_frame)
        action_frame.grid(row=3, column=0, columnspan=2, pady=10)

        draw_button = tk.Button(action_frame, text="Robar Carta", command=self.client.draw_card)
        draw_button.grid(row=0, column=0, padx=5)

        end_turn_button = tk.Button(action_frame, text="Terminar Turno", command=self.client.end_turn)
        end_turn_button.grid(row=0, column=1, padx=5)

    def update_gui(self, game_state):
        try:
            print(f"Actualizando GUI con el estado del juego: {game_state}")
            if 'players' in game_state and 'current_player' in game_state:
                for i, player in enumerate(game_state['players']):
                    stable_listbox = self.player_frames[i].winfo_children()[1]
                    stable_listbox.delete(0, tk.END)
                    for card in player['stable']:
                        stable_listbox.insert(tk.END, card['name'])

                if self.client.player_id:
                    current_player = next(player for player in game_state['players'] if player['id'] == self.client.player_id)
                    for i, button in enumerate(self.hand_buttons):
                        if i < len(current_player['hand']):
                            button.config(text=current_player['hand'][i]['name'])
                        else:
                            button.config(text="")
                    self.master.title(f"Unstable Unicorns - Turno de {game_state['current_player']}")
                else:
                    print("Player ID no está definido aún.")
            else:
                print("Datos incompletos en el estado del juego")
        except Exception as e:
            print(f"Error actualizando la GUI: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()
