import threading
import socket
import time

import rpyc
import json

import yaml
from flask import Flask
from flask_restful import reqparse, Api, Resource
from multiprocessing import Process


app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument('query', location='form')
parser.add_argument('api_key', location='form')

with open('config.yaml', 'r') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
    f.close()

coordinator_host = config['coordination']['host']
coordinator_port = config['coordination']['port']

connection = rpyc.connect(coordinator_host, coordinator_port, config={"sync_request_timeout": 240})

# listen on a socket for incoming connections using socket library
def ping_server(ahost, aport):
    """
    It creates a socket, binds it to a host and port, and listens for incoming connections.
    When a connection is made, it receives a message and prints it to the console.
    The message is sent from the client.
    :param ahost: the hostname of the server
    :param aport: the port number that the server will listen on
    """
    with open('key.txt', 'r') as f:
        key = f.readline()
        flag = int(key.split('=')[1])
        f.close()
    if flag == 0:
        print ('Starting Ping...')
        flag = 1
        # write key back to file
        with open('key.txt', 'w') as f:
            f.write('flag={}'.format(flag))
            f.close()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # bind the socket to a public host, and a well-known port
            s.bind((ahost, aport))
            s.listen()
            client_socket, address = s.accept()
            # become a server socket
            latest_ping_received = time.time()
            while True:
                # accept connections from outside
                client_socket.recv(1024).decode('utf-8')
                latest_ping_received = time.time() - latest_ping_received
                print("Time since last ping: ", latest_ping_received)


class Database(Resource, threading.Thread):
    def __init__(self):
        super().__init__()
        # self.client_socket = None
        self.get_message = None
        self.get_status_code = None
        self.post_message = None
        self.post_status_code = None
        self.api_key = '12345'

    def authenticate(self):
        """
        If the api_key is in the request, then return True, otherwise return False
        :return: True or False
        """
        args = parser.parse_args()
        print(args)
        try:
            api_key = args['api_key']
            if api_key == self.api_key:
                return True
        except KeyError:
            return False

    def get(self):
        """
        The function is a GET request that returns a message and a status code
        :return: The get method is returning a tuple of the get_message and get_status_code.
        """
        if self.authenticate():
            thread_obj = threading.Thread(target=self.dummy_get())
            thread_obj.start()
            return self.get_message, self.get_status_code
        else:
            return {'response': 'Authentication Failed'}, 401

    def dummy_get(self):
        """
        It takes a query, executes it, and returns the result
        """
        args = parser.parse_args()
        query = args['query'].lower()

        query_result = connection.root.execute_query(query)
        print("Thread ID for get: {}".format(threading.get_ident()))
        print("Query result: ", query_result)
        query_result = query_result.decode('utf-8')
        message, status_code = {'result': query_result}, 200
        self.get_message = message
        self.get_status_code = status_code

    def post(self):
        """
        The function is a POST request that takes in a JSON object, and if the authentication is successful,
        it starts a new thread that calls the dummy_post() function
        :return: The post method is returning a tuple of the post_message and post_status_code.
        """
        if self.authenticate():
            thread_obj = threading.Thread(target=self.dummy_post())
            thread_obj.start()
            return self.post_message, self.post_status_code
        else:
            return {'response': 'Authentication Failed'}, 401

    def dummy_post(self):
        """
        The function takes in a query, executes it, and returns a response
        """
        args = parser.parse_args()
        query = args['query'].lower()
        print("Thread ID for post: {}".format(threading.get_ident()))
        # time.sleep(1000)
        print(connection.root.execute_query(query))
        message, status_code = {'response': 'Query Executed'}, 200
        self.post_message = message
        self.post_status_code = status_code


api.add_resource(Database, '/databases')

# use multiprocessing module to run both flask and socket server
if __name__ == '__main__':
    host = config['app']['host']
    port = config['app']['port']
    ping_port = config['socket_ping']['port']
    backProc = Process(target=ping_server, args=(host, ping_port))
    backProc.start()
    app.run(debug=True, host=host, port=port)
    backProc.join()
