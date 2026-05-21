import socket

HOST = "127.0.0.1"
PORT = 5000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect((HOST, PORT))
    print('''\nType these words to issue commands:
    'record' - start recording footage
    'stop' - stop and save recording
    'focus + number' - adjust focus of camera (ex. focus 33) 
    'quit' - shutdown camera\n''')

    while True:
        
        text = input("Write a message ('quit' to quit): ")
        client.sendall(text.encode()) 

        data = client.recv(1024) 

        print("Server replied:" + str(data.decode().strip()) + '\n')

        if text.lower() == 'q':
            break