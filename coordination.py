import json
import re
import time
import rpyc
import yaml
from rpyc.utils.server import ThreadedServer
from rpyc.utils.factory import threading
import threading as thread
from db_conn import DBConnector
import socket


def ping_server(cphost, cpport):
    """
    It connects to the socket on the CP server and sends a message every 10 seconds
    
    :param cphost: The hostname of the server that the client will connect to
    :param cpport: The port that the client will connect to the server on
    """
    # connect to socket on 9002
    print("Starting ping server")
    print("Host: ", cphost, "Port: ", cpport)
    time.sleep(10)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((cphost, cpport))
        while True:
            print("Sending ping")
            time.sleep(10)
            try:
                s.sendall(b'I Am There!')
            except Exception as e:
                print("Error in sending ping: ", e)
                break


@rpyc.service
class Coordination1(rpyc.Service):
    def __init__(self, lock_connection):
        super().__init__()
        self.conn = None
        self.lock_connection = lock_connection
        self.rlock = threading.Lock()

    @rpyc.exposed
    def execute_query(self, query):
        """
        The function takes a query as input, connects to the database, acquires a lock, executes the query,
        and returns the result
        
        :param query: The query to be executed
        :return: The result of the query is being returned.
        """
        # get thread ID
        print("Thread ID: {}".format(threading.get_ident()))
        if query is None:
            return None
        try:
            # connect to DB
            table_name_hash = calculate_hash(query)
            # print("table name hash: ", table_name_hash)
            if table_name_hash != -1:
                database_id = "database" + str(1)  # str(random.choice([1, 2]))  # str(table_name_hash)
            else:
                database_id = "database3"
            db_conn_server = DBConnector(database_id)
            db_conn_server.connect()
            # execute query
            result = ''
            lock_status = self.lock_connection.root.acquire_lock(query)
            print("Lock status: ", lock_status)
            if lock_status:
                result = self.execute_new(query, db_conn_server)
            else:
                status = "Waiting for lock"
                while status == "Waiting for lock":
                    time.sleep(10)
                    if self.lock_connection.root.acquire_lock(query):
                        result = self.execute_new(query, db_conn_server)
                        status = "Lock acquired"

            if 'select' in query.lower():
                query_result_to_send = json.dumps(result, indent=2, default=str).encode()
            else:
                query_result_to_send = "Query Executed".encode()
                # commit changes
                db_conn_server.conn.commit()
            return query_result_to_send
        except Exception as exc:
            print('{}: {}'.format(type(exc).__name__, exc))
            err_dict = exc.__dict__
            return err_dict['msg'].encode()

    def execute_new(self, query, db_conn_server):
        # if 'insert' in query:
        #     print("Sleeping for 1000 seconds")
        #     time.sleep(100)
        self.rlock.acquire()
        result = db_conn_server.execute(query)
        # To delete start
        print("Query: ", query, "Thread ID: ", threading.get_ident())
        # To delete end
        self.rlock.release()
        self.lock_connection.root.release_lock(query)
        return result


def calculate_hash(query):
    if 'select' in query:
        pattern = re.compile(r'(?<=from\s)\w+')
    elif 'update' in query:
        pattern = re.compile(r'(?<=update\s)\w+')
    elif 'delete' in query:
        pattern = re.compile(r'(?<=delete\sfrom\s)\w+')
    elif 'create' in query:
        pattern = re.compile(r'(?<=create\stable\s)\w+')
    else:
        pattern = re.compile(r'(?<=insert\sinto\s)\w+')
    table_name = pattern.search(query)
    if table_name is not None:
        return hash(table_name) % 2 + 1
    else:
        return -1


if __name__ == '__main__':
    with open('key.txt', 'w') as f:
        f.write('flag=0')

    with open('config.yaml', 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    host = config['coordination']['host']
    port = config['coordination']['port']
    lock_manager_port = config['lock_manager']['port']
    lock_manager_host = config['lock_manager']['host']
    app_host = config['app']['host']
    ping_port = config['socket_ping']['port']

    print('Coordination Layer Started ...')
    lock_connection_main = rpyc.connect(lock_manager_host, lock_manager_port, config={"sync_request_timeout": 240})

    server = ThreadedServer(Coordination1(lock_connection_main), port=port, hostname=host)
    server = threading.Thread(target=server.start)
    ping = thread.Thread(target=ping_server, args=(app_host, ping_port))

    server.start()
    ping.start()


