from socket_conn import SocketConnectionServer
from db_conn import DBConnector


class ServerSocket:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = SocketConnectionServer(self.host, self.port)

    def run_server(self):
        while True:
            try:
                conn = self.sock.accept()
                data = conn.recv(1024).decode()
                print(f"Received query from Client")
                # connect to DB
                db_conn_server = DBConnector("ds_dummy")
                print("Connected to DB")
                db_conn_server.connect()
                # execute query
                result = db_conn_server.execute(data)
                # commit changes
                db_conn_server.conn.commit()
                conn.sendall("Query Executed".encode())

            except Exception as exc:
                print('{}: {}'.format(type(exc).__name__, exc))
        # conn.close()


if __name__ == '__main__':
    server = ServerSocket("localhost", 8080)
    server.run_server()
