import socket
import threading
import json
from logic_game import LogicGame

class GameServer:
    def __init__(self, host='127.0.0.1', port=5555):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.game = LogicGame()
        self.clients = []

    def start(self):
        self.server.listen(4)
        print(f"Server is listening on {self.host}:{self.port}")
        while True:
            try:
                conn, addr = self.server.accept()
                print(f"New connection from {addr}")
                if len(self.clients) < 4:
                    thread = threading.Thread(target=self.handle_client, args=(conn, addr))
                    thread.start()
                    print(f"Active connections: {len(self.clients)}")
                else:
                    print(f"Rejected connection from {addr}: maximum players reached")
                    conn.close()
            except Exception as e:
                print(f"Error accepting connection: {e}")
                break
        self.server.close()

    def handle_client(self, conn, addr):
        print(f"New connection from {addr}")
        player = self.game.add_player(f"Player_{len(self.clients)}")
        self.clients.append(conn)

        initial_message = json.dumps({"player_id": player.id}) + '\n'
        conn.send(initial_message.encode('utf-8'))

        while True:
            try:
                message = conn.recv(1024).decode('utf-8')
                if not message:
                    print(f"Connection closed by {addr}")
                    break
                print(f"Message from {addr}: {message.strip()}")
                message_json = json.loads(message)
                self.handle_message(message_json, player)
            except ConnectionResetError:
                print(f"Connection reset by {addr}. Closing connection.")
                break
            except Exception as e:
                print(f"Error handling message from {addr}: {e}")
                break

        conn.close()
        self.clients.remove(conn)
        print(f"Connection with {addr} closed. Active connections: {len(self.clients)}")

    def handle_message(self, message, player):
        if message['action'] == 'play_card':
            self.game.play_card(player.id, message['card_id'])
        elif message['action'] == 'draw_card':
            self.game.draw_card(player.id)
        elif message['action'] == 'end_turn':
            self.game.end_turn()
        self.broadcast_game_state()

    def broadcast_game_state(self):
        game_state = self.game.get_game_state()
        game_state_json = json.dumps(game_state) + '\n'
        for client in self.clients:
            try:
                client.send(game_state_json.encode('utf-8'))
            except Exception as e:
                print(f"Error broadcasting game state: {e}")

if __name__ == "__main__":
    server = GameServer()
    server.start()
