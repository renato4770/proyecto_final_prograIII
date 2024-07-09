import tkinter as tk
from tkinter import messagebox
from logic_game import LogicGame

class UnstableUnicornsGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Unstable Unicorns")
        self.game = LogicGame()

        self.player_frames = []
        self.hand_buttons = []

        self.setup_gui()

    def setup_gui(self):
        # Frame principal
        main_frame = tk.Frame(self.master)
        main_frame.pack(padx=10, pady=10)

        # Frames para cada jugador
        for i in range(4):
            player_frame = tk.LabelFrame(main_frame, text=f"Jugador {i+1}")
            player_frame.grid(row=i//2, column=i%2, padx=5, pady=5)
            self.player_frames.append(player_frame)

            # Establo del jugador
            stable_label = tk.Label(player_frame, text="Establo:")
            stable_label.pack()
            stable_listbox = tk.Listbox(player_frame, height=5)
            stable_listbox.pack()

        # Frame para la mano del jugador actual
        hand_frame = tk.LabelFrame(main_frame, text="Tu Mano")
        hand_frame.grid(row=2, column=0, columnspan=2, pady=10)

        # Botones para las cartas en la mano
        for i in range(5):
            card_button = tk.Button(hand_frame, text=f"Carta {i+1}", command=lambda i=i: self.play_card(i))
            card_button.grid(row=0, column=i, padx=2)
            self.hand_buttons.append(card_button)

        # Botones de acción
        action_frame = tk.Frame(main_frame)
        action_frame.grid(row=3, column=0, columnspan=2, pady=10)

        draw_button = tk.Button(action_frame, text="Robar Carta", command=self.draw_card)
        draw_button.grid(row=0, column=0, padx=5)

        end_turn_button = tk.Button(action_frame, text="Terminar Turno", command=self.end_turn)
        end_turn_button.grid(row=0, column=1, padx=5)

        # Iniciar el juego
        self.start_game()

    def start_game(self):
        for _ in range(4):
            self.game.add_player(f"Jugador {len(self.game.players)+1}")
        self.update_gui()

    def play_card(self, card_index):
        current_player = self.game.players[self.game.current_player_index]
        if card_index < len(current_player.hand):
            card = current_player.hand[card_index]
            self.game.play_card(current_player.id, card.id)
            self.update_gui()

    def draw_card(self):
        current_player = self.game.players[self.game.current_player_index]
        self.game.draw_card(current_player.id)
        self.update_gui()

    def end_turn(self):
        self.game.end_turn()
        self.update_gui()

    def update_gui(self):
        for i, player in enumerate(self.game.players):
            stable_listbox = self.player_frames[i].winfo_children()[1]
            stable_listbox.delete(0, tk.END)
            for card in player.stable:
                stable_listbox.insert(tk.END, card.name)

        current_player = self.game.players[self.game.current_player_index]
        for i, button in enumerate(self.hand_buttons):
            if i < len(current_player.hand):
                button.config(text=current_player.hand[i].name)
            else:
                button.config(text="")

        self.master.title(f"Unstable Unicorns - Turno de {current_player.id}")

if __name__ == "__main__":
    root = tk.Tk()
    app = UnstableUnicornsGUI(root)
    root.mainloop()