import socket
import sys 
import threading

class Client():
    def __init__(self):
        self.messaging_mode = 'all'
        self.messaged_user = ''
        
        self.run_state = True
        self.default = "\033[m"
        self.red = "\03391[m"
        
        self.nickname = sys.argv[1]
        # self.hostname  = sys.argv[1]
        # self.port = int(sys.argv[2])
         
        self.nick_len = len(self.nickname)
         
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = 5050
        
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.host, self.port))
    
    def receive(self):
        while True:
                try:
                    
                    # Receive messages from the server
                    message = self.client.recv(1024).decode('utf-8')
                    
                    # If client is disconnecting 
                    # Close connection 
                    # Break the loop 
                    if not self.run_state:
                        self.client.close()
                        break
                  
                   # If server does not have client nickname yet 
                   # Send nickname 
                    if message == 'nickname':
                        self.client.send(self.nickname.encode('utf-8'))
                    
                    # Print message to terminal if not empty
                    elif message:
                        print(f'{message}')
                
                # Error handling
                except:
                    # Let the user know
                    print("An error occured!")
                    # Close the connection 
                    self.client.close()
                    # Set run state to False
                    self.run_state = False
                    break
    
    def custom_input(self):
        pass
    
    def exit(self, message):
        self.run_state = False
        message = message.encode('utf-8')
        self.client.send(message)
    
    def all(self, message):
        # message = input(f'{self.nickname}:')
                    
        if message[self.nick_len+2:self.nick_len+6] == '/pm ':
            # print('ENTERED PM MODE')
            self.messaging_mode = 'pm'
            self.messaged_user = message[6+self.nick_len:]
            # print(f'{message}')
            self.messaged_user = str(len(self.messaged_user)) + self.messaged_user
            # print(f'{self.messaged_user}')
                    
        else:
            message = f'{message}'
            message = message.encode('utf-8')
            self.client.send(message)
         
    def send(self):
        while True:
            try:
                if self.run_state == False:
                    self.client.close
                    break
                
                message = '{}: {}'.format(self.nickname, input(''))
                if message:
                    print(f'PM CHECK {message[self.nick_len+2:self.nick_len+6]}')
                
                if message[-5:] == '/exit':
                    self.exit(message)
                    break
                    
                if self.messaging_mode == 'all':
                    # message = input(f'{self.nickname}:')
                    self.all()
                else:
                    
                    if message[self.nick_len+2:self.nick_len+6] == '/pm ':
                        self.messaged_user = message[6+self.nick_len:]
                        self.messaged_user = str(len(self.messaged_user)) + self.messaged_user
                    
                    elif message[self.nick_len+2:self.nick_len+6] == '/all':
                        self.messaging_mode = 'all'   
                    
                    else :
                        message = f'pm{self.messaged_user}{message}'
                        message = message.encode('utf-8')
                        self.client.send(message)
            except:
                self.run_state = False
                self.client.close()
                

client = Client()

receiving_thread = threading.Thread(target=client.receive)
receiving_thread.start()

send_thread = threading.Thread(target=client.send)
send_thread.start()



            