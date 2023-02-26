import json
import random
import re
import time

import rpyc
from rpyc.utils.server import ThreadedServer
from rpyc.utils.factory import threading
from db_conn import DBConnector


@rpyc.service
class Coordination1(rpyc.Service):
    def __init__(self):
        super().__init__()
        self.conn = None
        self.lock_connection = rpyc.connect('localhost', 9001)
        self.rlock = threading.Lock()
        self.lock_connection._config['sync_request_timeout'] = None

    @rpyc.exposed
    def execute_query(self, query):
        # get thread ID
        print("Thread ID: {}".format(threading.get_ident()))
        if query is None:
            return None
        try:
            # connect to DB
            table_name_hash = calculate_hash(query)
            # print("table name hash: ", table_name_hash)
            if table_name_hash != -1:
                database_id = "database" + str(1)#str(random.choice([1, 2]))  # str(table_name_hash)
            else:
                database_id = "database3"
            db_conn_server = DBConnector(database_id)
            # print("db name: ", db_conn_server.db_name)
            db_conn_server.connect()
            # print("Connected to DB")
            # execute query
            result = ''
            if self.lock_connection.root.acquire_lock(query):
                self.rlock.acquire()
                result = db_conn_server.execute(query)
                # To delete start
                if 'select' in query:
                    print("Sleeping for 1000 seconds")
                    time.sleep(1000)
                # To delete end
                self.rlock.release()
                self.lock_connection.root.release_lock(query)
            else:
                time.sleep(10)

            if 'select' in query.lower():
                query_result_to_send = json.dumps(result, indent=2, default=str).encode()
            else:
                query_result_to_send = "Query Executed".encode()
                # commit changes
                db_conn_server.conn.commit()
            # self.conn.sendall(query_result_to_send)
            return query_result_to_send
        except Exception as exc:
            print('{}: {}'.format(type(exc).__name__, exc))
            return exc


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


print('Coordination Layer Started ...')
server = ThreadedServer(Coordination1, port=9000)
server.start()
