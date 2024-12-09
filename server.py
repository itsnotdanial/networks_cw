import socket
import threading
import sys 

class Server:
    
    def __init__(self):
        self.clients = {}
        self.default = "\033[m"
        self.red = "\03391[m"
        # self.port = sys.argv[0]
        self.port = 5050
        self.host = socket.gethostbyname(socket.gethostname())
        
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()
            
    def broadcast(self, message, sender):
        # print('Looping to send message')
        for client in self.clients.values():
            if client != sender:
                client.send(message)
    
    def private_message(self, client, message):
        print('here pt3')
        client.send(message)
          
    def handle(self, client):
        while True:
            try:
                message = client.recv(1024)
                # T0DO MAKE FIRST TWO CHARS PM AND EXTRACT NICKNAME OF PM
                # CHECK HERE FOR THE FIRST TWO CHARS
                # IF FIRST 2 CHARS == PM THEN DO A PRIV MSG
                # CLIENT SIDE ISSUE
                print(message[:2])
                # print('Server has received message')
                # print(message[-5:])
                if message[-5:] == b'/exit':
                    self.close(client)
                    break
                
                elif message[:2] == b'pm':
                    print('here')
                    message = message.decode('utf-8')
                    leng = int(message[2]) + 2
                    nick = message[3:leng+1]
                    print(len(nick))
                    # print(self.clients)
                    # print(len(nick))
                    
                    try:
                        print('herept2')
                        receiver = self.clients[nick]
                        message = '[PRIVATE MESSAGE] ' + message[leng+1:]
                        message = message.encode('utf-8')
                        print('lolllhere')
                        self.private_message(receiver, message)
                        
                    
                    except:
                        message = f'{nick} doesnt exist wanker'.encode('utf-8')
                        client.send(message)
                               
                
                elif message:
                    self.broadcast(message, client)
           
            except:
                self.close(client)
                break
    
    def close(self, client):
        for key, value in self.clients.items():
            
            if value == client:
                print(f'{key} has dced')
                self.clients.pop(key)
                break
        client.close()
    
    def receive(self):
        while True:
            
            client, address = self.server.accept()
            client.send('nickname'.encode('utf-8'))
            # print('Server has asked for a name')
            
            nickname = client.recv(1024).decode('utf-8')
            message = f'Welcome {nickname}'.encode('utf-8')
            # print('Server is sending welcome message')
            client.send(message)
            
            connection_message = f'\n {nickname} has connected '
            connection_message= connection_message.encode('utf-8')
            self.broadcast(connection_message, client)
            
            self.clients[nickname] = client
            
            thread = threading.Thread(target=self.handle, args=(client,))
            thread.start()
    
    
                

server = Server()
print('Server is starting')
server.receive()
