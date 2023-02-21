import json
import socket
from socket_conn import SocketConnectionClient

from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource
# from socket_conn import SocketConnection

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('query', location='form')


class Database(Resource):
    def __init__(self):
        self.client_socket = None

    def get(self):
        self.client_socket = SocketConnectionClient("localhost", 8080)
        args = parser.parse_args()
        query = args['query'].lower()
        self.client_socket.send(query)
        query_result = self.client_socket.receive()

        query_result = json.loads(query_result)
        for row in query_result:
            print(row)

        message, status_code = {'response': 'Query Executed'}, 200
        self.client_socket.close()
        return message, status_code

    def post(self):
        self.client_socket = SocketConnectionClient("localhost", 8080)
        args = parser.parse_args()
        query = args['query'].lower()
        self.client_socket.send(query)
        _ = self.client_socket.receive()
        message, status_code = {'response': 'Query Executed'}, 200
        self.client_socket.close()
        return message, status_code


api.add_resource(Database, '/databases')

if __name__ == '__main__':
    app.run(debug=True)
