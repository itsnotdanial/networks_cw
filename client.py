import socket
import sys 
import threading

class Client():
    def __init__(self):
        self.nickname = sys.argv[0]
        self.hostname  = sys.argv[1]
        self.port = sys.argv[2]
        
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.hostname, self.port))
    
    def receive(self):
        while True:
                try:
                    # Receive Message From Server
                    # If 'NICK' Send Nickname
                    message = self.client.recv(1024).decode('utf-8')
                    if message == 'nickname':
                        self.client.send(self.nickname.encode('utf-8'))
                    else:
                        print(message)
                except:
                    # Close Connection When Error
                    print("An error occured!")
                    self.client.close()
                    break
            