import tkinter as tk
from tkinter import messagebox
import socket
import json
import threading
import time
from logic_game import LogicGame
#SERGIO 123
class UnstableUnicornsGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Unstable Unicorns")
        self.game = LogicGame()
        self.player_frames = []
        self.hand_buttons = []
        self.client = None
        self.connected = False
        self.player_id = None
        self.setup_network()
        self.setup_gui()

    def setup_network(self):
        self.connect_to_server()

    def connect_to_server(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            print("Intentando conectar al servidor...")
            self.client.connect(('127.0.0.1', 5555))
            self.connected = True
            print("Conectado al servidor")
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.start()
            heartbeat_thread = threading.Thread(target=self.send_heartbeat)
            heartbeat_thread.start()
        except ConnectionRefusedError:
            print("No se pudo conectar al servidor. Reintentando en 5 segundos...")
            self.master.after(5000, self.connect_to_server)
        except Exception as e:
            print(f"Error inesperado al conectar: {e}")
            self.master.after(5000, self.connect_to_server)

    def receive_messages(self):
        while self.connected:
            try:
                message = self.client.recv(1024).decode('utf-8')
                if not message:
                    print("Conexión cerrada por el servidor")
                    self.connected = False
                    break
                print(f"Mensaje recibido del servidor: {message}")
                game_state = json.loads(message)
                if 'player_id' in game_state:
                    self.player_id = game_state['player_id']
                self.master.after(0, self.update_gui, game_state)
            except json.JSONDecodeError:
                print("Error al decodificar el mensaje del servidor")
            except ConnectionError as e:
                print(f"Error de conexión: {e}")
                self.connected = False
                break
            except Exception as e:
                print(f"Error inesperado: {e}")
        print("Hilo de recepción terminado")
        self.master.after(5000, self.connect_to_server)

    def send_heartbeat(self):
        while self.connected:
            try:
                heartbeat = json.dumps({"action": "heartbeat"})
                print(f"Enviando latido: {heartbeat}")
                self.client.send(heartbeat.encode('utf-8'))
                time.sleep(5)  # Envía un latido cada 5 segundos
            except Exception as e:
                print(f"Error al enviar latido: {e}")
                self.connected = False
                break
        print("Hilo de latidos terminado")

    def send_message(self, message):
        if self.connected:
            try:
                print(f"Enviando mensaje: {message}")
                self.client.send(message.encode('utf-8'))
            except Exception as e:
                print(f"Error al enviar mensaje al servidor: {e}")
                self.connected = False
                self.master.after(5000, self.connect_to_server)
        else:
            print("No conectado al servidor. Reintentando conexión...")
            self.connect_to_server()

    def play_card(self, card_index):
        message = json.dumps({"action": "play_card", "card_id": card_index})
        self.send_message(message)

    def draw_card(self):
        message = json.dumps({"action": "draw_card"})
        self.send_message(message)

    def end_turn(self):
        message = json.dumps({"action": "end_turn"})
        self.send_message(message)

    def setup_gui(self):
        # Frame principal
        main_frame = tk.Frame(self.master)
        main_frame.pack(padx=10, pady=10)

        # Frames para cada jugador
        self.player_frames = []
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

    def update_gui(self, game_state):
        print(f"Actualizando GUI con el estado del juego: {game_state}")
        for i, player in enumerate(game_state['players']):
            stable_listbox = self.player_frames[i].winfo_children()[1]
            stable_listbox.delete(0, tk.END)
            for card in player['stable']:
                stable_listbox.insert(tk.END, card['name'])

        if self.player_id:
            current_player = next(player for player in game_state['players'] if player['id'] == self.player_id)
            for i, button in enumerate(self.hand_buttons):
                if i < len(current_player['hand']):
                    button.config(text=current_player['hand'][i]['name'])
                else:
                    button.config(text="")
            self.master.title(f"Unstable Unicorns - Turno de {game_state['current_player']}")
        else:
            print("Player ID no está definido aún.")

if __name__ == "__main__":
    root = tk.Tk()
    app = UnstableUnicornsGUI(root)
    root.mainloop()
