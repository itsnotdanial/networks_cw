import socket
import sys 
import threading
import os
import time
from io import StringIO

class Client():
    
    def __init__(self):
        # Initialize variables
        self.messaging_mode = 'all'
        self.messaged_user = ''
        
        self.run_state = True
        self.downloaded_files_list = []

        # Ensure user passes aruguments
        try:
            self.nickname = sys.argv[1]
        except IndexError:
            print('Please pick a nickname')
            sys.exit(1)  
        
        if self.nickname[0] == '/' or self.nickname[:2] ==  'pm':
            print('Please choose a nickname that does not begin with / or pm')
            sys.exit(1)
        
        try:
            self.hostname  = sys.argv[2]
        except IndexError:
            print('Please pick a hostname')
            sys.exit(1) 
        
        try:
            self.port = int(sys.argv[3])
        except:
            print('Please pick a valid port') 
            sys.exit(1)   
         
        self.nick_len = len(self.nickname)
        
        # Connect to the server
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client.connect((self.hostname, self.port))
        except:
            # Error message if unable to connect to the server
            print('The host/port is incorrect or the server is unavailable') 
            sys.exit(1)   
    
    def file_receive(self):
        
        # Receive header information from the client
        header = self.client.recv(1024).decode().strip()
        header = header.split('\n')
        size = int(header[0])
        filename = header[1]

        folder = self.nickname
        filepath = f'{self.nickname}/{filename}'
        
        # Create folder to save files if it doesn't exist
        os.makedirs(folder, exist_ok=True)
        
        # Continue receiving data until the entire file has been sent
        file_data = b''
        while len(file_data) < size:
            data_recv = self.client.recv(1024)
            file_data += data_recv 
        
        # Save the file
        with open(filepath, 'wb') as file:
            file.write(file_data)
        
        # Store the file name and its size     
        append_data = f'FILENAME : {filename} | SIZE : {str(size)} bytes'
        self.downloaded_files_list.append(append_data)
        
        print(f'{filename} has been successfully downloaded')
    
    def receive(self):
        while self.run_state:
            try:
                # Receive messages from the server
                message = self.client.recv(1024).decode('utf-8')
                 
                # Send nickname if requested
                if message == 'nickname':
                    self.client.send(self.nickname.encode('utf-8'))
                elif message == '/badnickname':
                    self.run_state = False
                    print('Pick a different nickname')
                # Break the receive loop if the client is exiting    
                elif message == '/exit':
                    print('Successfully exited')
                    self.run_state = False
                
                # Check if server is about to start sending data
                elif message == '/download':
                    # Handles download
                    self.file_receive()
                
                # Display message if the file requested does not exist
                elif message == '/notexist':
                    print('The file you requested does not exist')
                
                # Print chat messages to the console if they're not empty
                elif message:
                    print(f'{message}')
            
            # Error handling
            except Exception as e:
                # Print error message and break the loop
                print(f"The following error has occured : {e}")
                self.run_state = False
        
        
        # Close the connection
        sys.stdin = StringIO('close')      
        self.client.close()
    
    def command(self, message):
        # Send a command to the server
        message = message.encode('utf-8')
        self.client.send(message) 
    
    def downloadedfiles(self):
        # Display downloaded files and their file size
        if len(self.downloaded_files_list) != 0:
            for file_data in self.downloaded_files_list:
                print(file_data)
        else:
            print('No files have been downloaded')    
            
    def all_mode(self, message):
        # Check if the client wants to private message a user  
        if message[:4] == '/pm ':
            # Switch to private messaging mode
            self.messaging_mode = 'pm'
            self.messaged_user = message[4:]
            
            # Store the current user being messaged
            self.messaged_user = str(len(self.messaged_user)) + self.messaged_user
            
        else:
            # Send message to be broadcasted to the server
            message = f'{self.nickname}: {message}'
            message = message.encode('utf-8')
            self.client.send(message)    
    
    def private_message(self, message):
        # Check if the client wants to private message a different user
        if message[:4] == '/pm ':
            # Switch the current privately messaged user
            self.messaged_user = message[4:]
            self.messaged_user = str(len(self.messaged_user)) + self.messaged_user
        
        # Check if the client wants to switch to broadcast mode          
        elif message == '/all':
            # Switch to broadcast mode
            self.messaging_mode = 'all'   
        
        else :
            # Continue private messaging the same user
            message = f'pm{self.messaged_user}{self.nickname}: {message}'
            message = message.encode('utf-8')
            self.client.send(message)
            
    def send(self):
        while self.run_state:
            try:
                # 0.1 second delay to fix formatting
                time.sleep(0.1)
                
                message = input()
                 
                if message == '/exit':
                    # Exit the program
                    self.command(message)
                    break
                
                elif message == '/access':
                    # Request access from server
                    self.command(message)      
                
                elif message == '/listsharedfiles':
                    # Request list of files from server
                    self.command(message)    
                
                elif message[:10] == '/download ':
                    # Request file download from the server
                    self.command(message)           
                
                elif message == '/downloadedfiles':
                    # Display locally downloaded files
                    self.downloadedfiles()
                                   
                elif self.messaging_mode == 'all':
                    # Handles messages for all mode
                    self.all_mode(message)
    
                else:
                    # Handles messages for private mode
                    self.private_message(message)
            
            except:
                # Break the loop and close the connection
                self.run_state = False        

client = Client()

receiving_thread = threading.Thread(target=client.receive)
receiving_thread.start()

send_thread = threading.Thread(target=client.send)
send_thread.start()



            