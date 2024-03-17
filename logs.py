import socket

print("Waiting for log messages...")


while True:
    try:
        server_address = ('localhost', 9000)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(server_address)
        sock.listen(1)

        connection, client_address = sock.accept()
        while True:
            data = connection.recv(1024)
            if not data:
                break
            log_message = data.decode('utf-8')
            print("LOG:", log_message)

        connection.close()
        sock.close()
    except:
        pass