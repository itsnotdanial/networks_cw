import socket
import threading
import sys 

class Server:
    
    def __init__(self):
        self.clients = {}
        self.port = sys.argv[0]
        self.host_ip = '127.0.0.1'
        
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
            
            
    def broadcast(self, message):
        for client in self.clients.values:
            client.send(message)
            
        
    def handle(self, client):
        while True:
            try:
                message = client.recv(1024)
                self.broadcast(message).encode('utf-8')
            except:
                self.close(client)
    
    def close(self, client):
        message = f"{self.clients[client]} has disconnected :("
        self.broadcast(message)
        self.clients[client].pop()
        client.close()
    
    def receive(self):
        while True:
            
            client, address = self.server.accept()
            client.send('nickname'.encode('utf-8'))
            
            nickname = client.recv(1024).decode('utf-8')
            client.send(f'Welcome {nickname}!').encode('utf-8')
            self.clients[client] = nickname
            
            connection_message = f'{nickname} has connected '
            self.broadcast(connection_message)
            
            self.clients[client] = nickname
            
            thread = threading.Thread(target=self.handle, args=(client,))
            thread.start()
            