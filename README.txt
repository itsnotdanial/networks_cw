Chatroom 

- This program features a CLI chatroom with a client-server architecture
- By default the program starts in broadcast mode

Starting the server & client 
    
    python server.py [port]  
        - Starts the server
        - [port] : Port the server is to run on 
    
    python client.py [username] [hostname] [port number] 
        - Starts the client 
        - [username] : The chatroom display name for the client
        - [hostname] : The IP address that the server is running on
        - [port] : The port the server is running on 

Chatroom commands
    
    /pm [username] 
        - Switches to private messageing mode 
        - [username] the user to be privately messaged
    
    /all 
        - Switches to broadcast mode
    
    /access 
        - Requests shared file access from the server
    
    /listsharedfiles 
        - Requests a list of the shared file from the server
    
    /download [filename] 
        - Sends a request to download a file from the server
        - [filename] : The file to be downloaded from the server
    
    /downloadedfiles 
        - Displays the downloaded files with their filesize

    /exit 
        - Disconnects from the chatroom