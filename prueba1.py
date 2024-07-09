import tkinter as tk
from tkinter import simpledialog, messagebox
import socket
import threading

class GameClient:
    def __init__(self, master):
        self.master = master
        self.master.title("Unstable Unicorns")
        self.master.geometry("400x300")

        self.server_ip = simpledialog.askstring("Input", "Server IP:", parent=self.master)
        self.server_port = 12345

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.server_ip, self.server_port))

        self.chat_box = tk.Text(master, state='disabled')
        self.chat_box.pack(pady=10)

        self.msg_entry = tk.Entry(master, width=50)
        self.msg_entry.pack(pady=10)
        self.msg_entry.bind("<Return>", self.send_message)

        self.recv_thread = threading.Thread(target=self.receive_messages)
        self.recv_thread.daemon = True
        self.recv_thread.start()

    def send_message(self, event=None):
        msg = self.msg_entry.get()
        self.client.send(msg.encode('utf-8'))
        self.msg_entry.delete(0, tk.END)

    def receive_messages(self):
        while True:
            try:
                msg = self.client.recv(1024).decode('utf-8')
                self.chat_box.config(state='normal')
                self.chat_box.insert(tk.END, msg + "\n")
                self.chat_box.config(state='disabled')
            except:
                messagebox.showerror("Error", "Conexión al servidor perdida")
                self.client.close()
                break

if __name__ == "__main__":
    root = tk.Tk()
    app = GameClient(root)
    root.mainloop()
