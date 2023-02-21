import json
import threading
from _thread import start_new_thread

from socket_conn import SocketConnectionServer
from db_conn import DBConnector


class ServerSocket(threading.Thread):
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.sock = SocketConnectionServer(self.host, self.port)

    def run_thread(self):
        print(f"Server listening on {self.host}:{self.port}")
        while True:
            # Start a new thread
            conn = self.sock.accept()
            print("Accepted connection from client")
            client_query = conn.recv(1024).decode()
            print(f"Received query from Client")
            # thread_obj = threading.Thread(target=self.run_server(conn))
            # thread_obj.start()
            start_new_thread(self.run_server(client_query), ())
            # print thread ID
            print("Thread ID: {}".format(threading.get_ident()))

    def run_server(self, client_query):
        print(f"Received query from Client")
        try:
            # connect to DB
            db_conn_server = DBConnector("ds_dummy")
            print("Connected to DB")
            db_conn_server.connect()
            # execute query
            result = db_conn_server.execute(client_query)
            if 'select' in client_query.lower():
                query_result_to_send = json.dumps(result, indent=2, default=str).encode()
            else:
                query_result_to_send = "Query Executed".encode()
                # commit changes
                db_conn_server.conn.commit()
            conn.sendall(query_result_to_send)
        except Exception as exc:
            print('{}: {}'.format(type(exc).__name__, exc))


if __name__ == '__main__':
    server = ServerSocket("localhost", 8080)
    server.run_thread()
