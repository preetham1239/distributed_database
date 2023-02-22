import json

import rpyc
from rpyc.utils.server import ThreadedServer
from rpyc.utils.factory import threading
from db_conn import DBConnector


@rpyc.service
class Coordination1(rpyc.Service):
    @rpyc.exposed
    def execute_query(self, query):
        # get thread ID
        print("Thread ID: {}".format(threading.get_ident()))
        if query is None:
            return None
        try:
            # connect to DB
            db_conn_server = DBConnector("ds_dummy")
            print("Connected to DB")
            db_conn_server.connect()
            # execute query
            result = db_conn_server.execute(query)
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


print('starting server')
server = ThreadedServer(Coordination1, port=9000)
server.start()

# git commit -m "Moved to RPC. Both app and coordination layer work with threads as expected.