import socket
import threading
import sys
import os 

SERVER_SHARED_FILES = os.getenv('SERVER_SHARED_FILES', os.path.join(os.getcwd(), 'SharedFiles'))

class Server:
    
    def __init__(self):
        self.clients = {}
        
        # Ensures port number has been passed 
        try:
            self.port = int(sys.argv[1])
        except Exception:
            print('Please provide a valid port number')
            sys.exit(1)  
        
        # Sets the server up
        self.host = socket.gethostbyname(socket.gethostname())
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self.server.bind((self.host, self.port))   
        self.server.listen()
        
        print(f'Server is running on {self.host}') 
    
    def broadcast(self, message, sender):
        # Broadcasts message to all connected clients other than the sender
        for client in self.clients.values():
            if client != sender:
                client.send(message)
    
    def private_message(self, client, message):
        # Sends a private message to the specified user
        client.send(message)
    
    def access(self, client):
        # Counts the number of files and sends it back to the user
        try:
            file_list = os.listdir(SERVER_SHARED_FILES)

            files_len = len(file_list)
        
            message = f'Access granted. {files_len} files are in the folder'.encode('utf-8')
            client.send(message)
        except:
            message = f'Folder does not exist'.encode('utf-8')
            client.send(message)        
    
    def listsharedfiles(self, client):
        # Sends all the names of the files in the shared user folder
        try:
            file_list = os.listdir(SERVER_SHARED_FILES)
            message = ''

            for file in file_list:
                message =  message + ' ' + file
            message = message.encode('utf-8')
            client.send(message)   
        except:
            message = 'Folder is empty'.encode('utf-8')
            client.send(message)
    
    def send_file(self, client, filename):
        try:
            filename = filename.decode('utf-8')
            # Opens the file that was requested
            file = open(f'{SERVER_SHARED_FILES}/{filename}', 'rb')
            
            # Calculates size of requested file
            size = os.path.getsize(f'{SERVER_SHARED_FILES}/{filename}')
            size = str(size)
            
            # Indication that the server is about to start sending data
            client.send(b'/download')
            
            # Header data for file
            header = f'{size}\n{filename}'.encode('utf-8')
            client.send(header)
            
            # Reads file
            file_data = file.read()
            file.close()
            
            # Sends file to the client 
            client.sendall(file_data)
        
        except:
            # Tells the client the file requested does not exist
            client.send(b'/notexist') 
                
    def handle(self, client):
        access = False
        while True:
            try:
                # Receives message from the client
                message = client.recv(1024)
                
                # Check if the client wants to leave
                if message == b'/exit':
                    # Tell the client that the server is closing the connection
                    client.send(message)
                    self.close(client)
                    break
                
                # Check if the client is requesting access to the shared files
                elif message == b'/access':
                    # Grant access
                    access = True
                    self.access(client)
                
                # Check if the client is requesting a list of the shared files
                elif message == b'/listsharedfiles':
                    # Check if the client has access
                    if access:
                        # Send the list of files
                        self.listsharedfiles(client)
                    else:
                        # Tell the client they don't have access
                        message = 'You do not have access'.encode('utf-8')
                        client.send(message)    
                
                # Check if the client has requested a file
                elif message[:10] == b'/download ':
                    # Check if the client has access
                    if access:
                        # Send the file
                        self.send_file(client, message[10:])
                    else:
                        # Tell the client they don't have access
                        message = 'You do not have access'.encode('utf-8')
                        client.send(message)   
                
                # Check if the client is private messaging someone       
                elif message[:2] == b'pm':
                    message = message.decode('utf-8')
                    # Extract the nickname of the client they are trying to message
                    leng = int(message[2]) + 2
                    nick = message[3:leng+1]
                    
                    try:
                        # Send the client's message to the requested client
                        receiver = self.clients[nick]
                        message = '[PRIVATE MESSAGE] ' + message[leng+1:]
                        message = message.encode('utf-8')
                        self.private_message(receiver, message)
                    
                    except:
                        # Tell the client the requested client does not exist
                        message = f'{nick} does not exist'.encode('utf-8')
                        client.send(message)
                               
                elif message:
                    # Broadcast the message if it is not empty
                    self.broadcast(message, client)
           
            except:
                # Close the connection if there is an error
                self.close(client)
                break
    
    def close(self, client):
        for key, value in self.clients.items():
            
            if value == client:
                # Broadcast that the client has left
                message = (f'{key} has left')
                message = message.encode('utf-8')
                self.broadcast(message, client)
                
                # Remove the client from the connected client dictionary
                self.clients.pop(key)
                break
        
        client.close()
    
    def receive(self):
        while True:
            # Accept new connections
            client, address = self.server.accept()
            # Ask for a username
            client.send('nickname'.encode('utf-8'))
            
            nickname = client.recv(1024).decode('utf-8')
            # Check if the username is already in use
            if nickname in self.clients:
                # Ask the client to pick a different username
                message = f'/badnickname'.encode('utf-8')
                client.send(message)
                client.close()
            else:
                print(f'IP Address : {address[0]} || Port Number : {address[1]}')
                
                # Send welcome message
                message = f'Welcome {nickname}'.encode('utf-8')
                client.send(message)
                
                # Broadcast a new client has joined
                connection_message = f'{nickname} has joined'
                connection_message= connection_message.encode('utf-8')
                self.broadcast(connection_message, client)
                
                # Add new client to dictionary
                self.clients[nickname] = client
                
                # Handle the new client in a seperate thread
                thread = threading.Thread(target=self.handle, args=(client,))
                thread.start()

    
                

server = Server()
server.receive()
