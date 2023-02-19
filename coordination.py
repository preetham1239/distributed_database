from socket_conn import SocketConnectionServer
from db_conn import DBConnector


class ServerSocket:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = SocketConnectionServer(self.host, self.port)

    def run_server(self):
        print("Five")
        while True:
            conn = self.sock.accept()
            data = conn.recv(1024)
            print(f"Received {data!r} from Client")
            # connect to DB
            # execute query
            # db_conn_server = DBConnector("ds_dummy")
            # db_conn_server.connect()
            # execute query
            # cursor = db_conn_server.conn.cursor()

            conn.sendall(data)
        # conn.close()


if __name__ == '__main__':
    server = ServerSocket("localhost", 8080)
    server.run_server()