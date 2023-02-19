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
        return {'data': "data"}, 200

    def post(self):
        self.client_socket = SocketConnectionClient("localhost", 8080)
        args = parser.parse_args()
        query = args['query']
        self.client_socket.send(query)
        self.client_socket.receive()
        message, status_code = {'response': 'Query Executed'}, 200
        return message, status_code


api.add_resource(Database, '/databases')

if __name__ == '__main__':
    app.run(debug=True)
