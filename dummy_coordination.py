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
        self.conn = None
        self.client_query = None

    def run_thread(self):
        print(f"Server listening on {self.host}:{self.port}")
        while True:
            # Start a new thread
            self.conn = self.sock.accept_clients()
            self.client_query = self.conn.recv(1024).decode()
            print(f"Received query from client: {self.client_query}")
            # self.run_server()
            thread_obj1 = threading.Thread(target=self.run_server)
            thread_obj1.start()
            # start_new_thread(self.run_server(client_query), ())
            # print thread ID

    def run_server(self):
        print("Thread ID: {}".format(threading.get_ident()))
        if self.client_query is None:
            pass
        try:
            # connect to DB
            db_conn_server = DBConnector("ds_dummy")
            print("Connected to DB")
            db_conn_server.connect()
            # execute query
            result = db_conn_server.execute(self.client_query)
            if 'select' in self.client_query.lower():
                query_result_to_send = json.dumps(result, indent=2, default=str).encode()
            else:
                query_result_to_send = "Query Executed".encode()
                # commit changes
                db_conn_server.conn.commit()
            self.conn.sendall(query_result_to_send)
        except Exception as exc:
            print('{}: {}'.format(type(exc).__name__, exc))


if __name__ == '__main__':
    server = ServerSocket("localhost", 8080)
    server.run_thread()
