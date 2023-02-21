import socket


class SocketConnectionClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))

    def send(self, data=str):
        data_to_send = data.encode()
        self.sock.sendall(data_to_send)
        print(f"Sent query to co-ordination layer")

    def receive(self):
        data = self.sock.recv(1024).decode()
        # print(data)
        return data

    def close(self):
        self.sock.close()
        print("Client Socket Closed")


class SocketConnectionServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen()

    def accept(self):
        conn, addr = self.sock.accept()
        print(f"Connected by client: {addr}")
        return conn

    def close(self):
        self.sock.close()
        print("Server Socket Closed")
