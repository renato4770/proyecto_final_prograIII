import socket
import threading

class GameServer:
    def __init__(self, host='127.0.0.1', port=12345):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(4)
        self.clients = []
        self.max_players = 4
        self.lock = threading.Lock()

    def handle_client(self, client_socket, addr):
        print(f"Conexión de {addr} establecida.")
        while True:
            try:
                msg = client_socket.recv(1024).decode('utf-8')
                if not msg:
                    break
                self.broadcast(msg, client_socket)
            except:
                self.clients.remove(client_socket)
                client_socket.close()
                break
        print(f"Conexión de {addr} terminada.")

    def broadcast(self, msg, client_socket):
        with self.lock:
            for client in self.clients:
                if client != client_socket:
                    try:
                        client.send(msg.encode('utf-8'))
                    except:
                        client.close()
                        self.clients.remove(client)

    def start(self):
        print("Servidor iniciado...")
        while len(self.clients) < self.max_players:
            client_socket, addr = self.server.accept()
            self.clients.append(client_socket)
            thread = threading.Thread(target=self.handle_client, args=(client_socket, addr))
            thread.start()

if __name__ == "__main__":
    server = GameServer()
    server.start()
