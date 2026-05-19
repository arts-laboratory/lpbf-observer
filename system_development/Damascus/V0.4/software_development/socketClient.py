import socket

HOST = "127.0.0.1"
PORT = 5000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect((HOST, PORT))

    while True:
        text = input("Write a message ('q' to quit): ")
        client.sendall(text.encode())

        data = client.recv(1024) 

        print("Server replied:", data.decode().strip())

        if text.lower() == 'q':
            break