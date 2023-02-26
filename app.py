import threading
import time

import rpyc
import json
from flask import Flask
from flask_restful import reqparse, Api, Resource

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('query', location='form')


class Database(Resource, threading.Thread):
    def __init__(self):
        super().__init__()
        # self.client_socket = None
        self.get_message = None
        self.get_status_code = None
        self.post_message = None
        self.post_status_code = None

    def get(self):
        thread_obj = threading.Thread(target=self.dummy_get())
        thread_obj.start()
        return self.get_message, self.get_status_code
        # thread_obj.

    def dummy_get(self):
        connection = rpyc.connect('localhost', 9000)
        args = parser.parse_args()
        query = args['query'].lower()

        query_result = connection.root.execute_query(query)
        print("Thread ID for get: {}".format(threading.get_ident()))
        print(query_result)
        query_result = json.loads(query_result)
        # for row in query_result:
        #     print(row)

        message, status_code = {'result': query_result}, 200
        self.get_message = message
        self.get_status_code = status_code

    def post(self):
        thread_obj = threading.Thread(target=self.dummy_post())
        thread_obj.start()
        return self.post_message, self.post_status_code

    def dummy_post(self):
        connection = rpyc.connect('localhost', 9000)
        args = parser.parse_args()
        query = args['query'].lower()
        print("Thread ID for post: {}".format(threading.get_ident()))
        print(connection.root.execute_query(query))
        message, status_code = {'response': 'Query Executed'}, 200
        self.post_message = message
        self.post_status_code = status_code


api.add_resource(Database, '/databases')

if __name__ == '__main__':
    app.run(debug=True)
