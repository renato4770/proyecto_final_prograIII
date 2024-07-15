import socket
import threading
import tkinter as tk
import json
import time
from logic_game import LogicGame
from game_state import GameState

class Client:
    def __init__(self, host, port, gui):
        self.server_host = host
        self.server_port = port
        self.sock = None
        self.receive_thread = None
        self.heartbeat_thread = None
        self.game_state = GameState()
        self.gui = gui
        self.player_id = None
        self.connected = False

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            print("Intentando conectar al servidor...")
            self.sock.connect((self.server_host, self.server_port))
            self.connected = True
            print("Conectado al servidor")
            self.receive_thread = threading.Thread(target=self.receive_messages)
            self.receive_thread.start()
            self.heartbeat_thread = threading.Thread(target=self.send_heartbeat)
            self.heartbeat_thread.start()
        except ConnectionRefusedError:
            print("No se pudo conectar al servidor. Reintentando en 5 segundos...")
            self.gui.master.after(5000, self.connect)
        except Exception as e:
            print(f"Error inesperado al conectar: {e}")
            self.gui.master.after(5000, self.connect)

    def receive_messages(self):
        buffer = ""
        while self.connected:
            try:
                data = self.sock.recv(1024).decode('utf-8')
                if not data:
                    print("Conexión cerrada por el servidor")
                    self.connected = False
                    break
                buffer += data
                while '\n' in buffer:
                    message, buffer = buffer.split('\n', 1)
                    print(f"Mensaje recibido del servidor: {message}")
                    game_state = json.loads(message)
                    if 'player_id' in game_state:
                        self.player_id = game_state['player_id']
                    self.gui.master.after(0, self.gui.update_gui, game_state)
            except json.JSONDecodeError:
                print("Error al decodificar el mensaje del servidor")
            except ConnectionError as e:
                print(f"Error de conexión: {e}")
                self.connected = False
                break
            except Exception as e:
                print(f"Error inesperado: {e}")
        print("Hilo de recepción terminado")
        self.gui.master.after(5000, self.connect)

    def send_heartbeat(self):
        while self.connected:
            try:
                heartbeat = json.dumps({"action": "heartbeat"}) + '\n'
                print(f"Enviando latido: {heartbeat.strip()}")
                self.sock.send(heartbeat.encode('utf-8'))
                time.sleep(5)
            except Exception as e:
                print(f"Error al enviar latido: {e}")
                self.connected = False
                break
        print("Hilo de latidos terminado")

    def send_message(self, message):
        if self.connected:
            try:
                message_with_newline = message + '\n'
                print(f"Enviando mensaje: {message_with_newline.strip()}")
                self.sock.send(message_with_newline.encode('utf-8'))
            except Exception as e:
                print(f"Error al enviar mensaje al servidor: {e}")
                self.connected = False
                self.gui.master.after(5000, self.connect)
        else:
            print("No conectado al servidor. Reintentando conexión...")
            self.connect()

    def play_card(self, card_id):
        message = json.dumps({"action": "play_card", "card_id": card_id})
        self.send_message(message)

    def draw_card(self):
        message = json.dumps({"action": "draw_card"})
        self.send_message(message)

    def end_turn(self):
        message = json.dumps({"action": "end_turn"})
        self.send_message(message)

# class GameState:
#     def __init__(self):
#         self.players = []
#         self.current_player = None

#     def update_state(self, state):
#         self.players = state['players']
#         self.current_player = state['current_player']

#     def get_state(self, player_id):
#         return {
#             'players': self.players,
#             'current_player': self.current_player,
#             'player_id': player_id
#         }

# class GUI:
#     def __init__(self, master):
#         self.master = master
#         self.master.title("Unstable Unicorns")
#         self.game = LogicGame()
#         self.player_frames = []
#         self.hand_buttons = []
#         self.client = Client('127.0.0.1', 5555, self)
#         self.player_id = None
#         self.setup_network()
#         self.setup_gui()

#     def setup_network(self):
#         self.client.connect()

#     def setup_gui(self):
#         main_frame = tk.Frame(self.master)
#         main_frame.pack(padx=10, pady=10)

#         self.player_frames = []
#         for i in range(4):
#             player_frame = tk.LabelFrame(main_frame, text=f"Jugador {i+1}")
#             player_frame.grid(row=i//2, column=i%2, padx=5, pady=5)
#             self.player_frames.append(player_frame)

#             stable_label = tk.Label(player_frame, text="Establo:")
#             stable_label.pack()
#             stable_listbox = tk.Listbox(player_frame, height=5)
#             stable_listbox.pack()

#         hand_frame = tk.LabelFrame(main_frame, text="Tu Mano")
#         hand_frame.grid(row=2, column=0, columnspan=2, pady=10)

#         for i in range(5):
#             card_button = tk.Button(hand_frame, text=f"Carta {i+1}", command=lambda i=i: self.client.play_card(i))
#             card_button.grid(row=0, column=i, padx=2)
#             self.hand_buttons.append(card_button)

#         action_frame = tk.Frame(main_frame)
#         action_frame.grid(row=3, column=0, columnspan=2, pady=10)

#         draw_button = tk.Button(action_frame, text="Robar Carta", command=self.client.draw_card)
#         draw_button.grid(row=0, column=0, padx=5)

#         end_turn_button = tk.Button(action_frame, text="Terminar Turno", command=self.client.end_turn)
#         end_turn_button.grid(row=0, column=1, padx=5)

#     def update_gui(self, game_state):
#         try:
#             print(f"Actualizando GUI con el estado del juego: {game_state}")
#             if 'players' in game_state and 'current_player' in game_state:
#                 for i, player in enumerate(game_state['players']):
#                     stable_listbox = self.player_frames[i].winfo_children()[1]
#                     stable_listbox.delete(0, tk.END)
#                     for card in player['stable']:
#                         stable_listbox.insert(tk.END, card['name'])

#                 if self.client.player_id:
#                     current_player = next(player for player in game_state['players'] if player['id'] == self.client.player_id)
#                     for i, button in enumerate(self.hand_buttons):
#                         if i < len(current_player['hand']):
#                             button.config(text=current_player['hand'][i]['name'])
#                         else:
#                             button.config(text="")
#                     self.master.title(f"Unstable Unicorns - Turno de {game_state['current_player']}")
#                 else:
#                     print("Player ID no está definido aún.")
#             else:
#                 print("Datos incompletos en el estado del juego")
#         except Exception as e:
#             print(f"Error actualizando la GUI: {e}")

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = GUI(root)
#     root.mainloop()
