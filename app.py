import socket
from socket_conn import SocketConnectionClient

from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource
# from socket_conn import SocketConnection

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('query', location='form')


class Todo(Resource):
    def __init__(self):
        self.client_socket = None

    def get(self):
        return {'data': "data"}, 200

    def post(self):
        print("One")
        self.client_socket = SocketConnectionClient("localhost", 8080)
        print("Two")
        args = parser.parse_args()
        print("Three")
        query = args['query']
        print("Four")
        self.client_socket.send(b"Hello, server")
        print("Eight")
        data = self.client_socket.receive()
        print("Nine")
        # print(f"Received {data!r}")
        print("Ten")
        message, status_code = {'response': 'Query Executed'}, 200
        print("Eleven")
        return message, status_code


# # TodoList
# # shows a list of all todos, and lets you POST to add new tasks
# class TodoList(Resource):
#     def get(self):
#         return TODOS
#
#     def post(self):
#         args = parser.parse_args()
#         todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
#         todo_id = 'todo%i' % todo_id
#         TODOS[todo_id] = {'task': args['task']}
#         return TODOS[todo_id], 201


# api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos')

if __name__ == '__main__':
    app.run(debug=True)
