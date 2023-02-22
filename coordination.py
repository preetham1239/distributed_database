import json
import random
import re

import rpyc
from rpyc.utils.server import ThreadedServer
from rpyc.utils.factory import threading
from db_conn import DBConnector


@rpyc.service
class Coordination1(rpyc.Service):
    def __init__(self):
        super().__init__()
        self.conn = None
        self.lock = threading.Lock()

    @rpyc.exposed
    def execute_query(self, query):
        # get thread ID
        print("Thread ID: {}".format(threading.get_ident()))
        if query is None:
            return None
        try:
            # connect to DB
            table_name_hash = calculate_hash(query)
            print("table name hash: ", table_name_hash)
            if table_name_hash != -1:
                database_id = "database" + str(random.choice([1, 2]))  # str(table_name_hash)
            else:
                database_id = "database3"
            db_conn_server = DBConnector(database_id)
            # print("db name: ", db_conn_server.db_name)
            db_conn_server.connect()
            print("Connected to DB")
            # execute query
            self.lock.acquire()
            result = db_conn_server.execute(query)
            self.lock.release()
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


print('starting server')
server = ThreadedServer(Coordination1, port=9000)
server.start()
