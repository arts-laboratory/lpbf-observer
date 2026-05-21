import socket

HOST = "127.0.0.1"
PORT = 5000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((HOST, PORT))
    server.listen(1)
    print(f"Listening on {HOST}:{PORT}")

    isRecording = False

    while True:
        connect, address = server.accept()
        print("Continuously connected by", address)
        while True:
            dataRec = connect.recv(1024)
            if dataRec.decode().strip().lower() == "q":
                print(b"Closing")
                connect.sendall(b"Closing\n")
                server.close()
            elif dataRec.decode().strip().lower() == 'record' and isRecording == False:
                print(f"Begin recording\n")
                connect.sendall(b"STATUS - Recording\n")
                isRecording = True
            elif dataRec.decode().strip().lower() == 'stop':
                print("Stopped recording\n")
                connect.sendall(b"STATUS - Recording stopped\n")
                isRecording = False
            elif dataRec.decode().strip().lower() == 'record' and isRecording == True:
                print("Already recording\n")
                connect.sendall(b"STATUS - Currently recording\n")
