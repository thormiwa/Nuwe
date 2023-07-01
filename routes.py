from flask_restful import Api, Resource, reqparse
import bcrypt
from db import create_connection, close_connection


class Register(Resource):
    def post(self):
        conn = create_connection()
        parser = reqparse.RequestParser()

        parser.add_argument('first_name', required=True)
        parser.add_argument('last_name', required=True)
        parser.add_argument('username', required=True)
        parser.add_argument('password', required=True)

        args = parser.parse_args()
        first_name = args['first_name']
        last_name = args['last_name']
        username = args['username']
        password = args['password']

        hashed_password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        db_cursor = conn.cursor()
        db_cursor.execute('INSERT INTO users (first_name, last_name, username, password) VALUES (?, ?, ?, ?)', (first_name, last_name, username, hashed_password))
        conn.commit()
        db_cursor.close()
        close_connection(conn)

        return {'message': 'User {} was created successfully'.format(username)}, 201

class Login(Resource):
    def post(self):
        conn = create_connection()
        parser = reqparse.RequestParser()

        parser.add_argument('username', required=True)
        parser.add_argument('password', required=True)

        args = parser.parse_args()
        username = args['username']
        password = args['password']

        db_cursor = conn.cursor()
        db_cursor.execute('SELECT id, username, password FROM users WHERE username = ?', (username,))
        user = db_cursor.fetchone()

        if user:
            stored_hash = user[2]
            if bcrypt.checkpw(password.encode('utf8'), stored_hash):
                data = {'message': 'User {} was logged in successfully'.format(user[1])}
            else:
                data = {'error': 'Invalid credentials'}, 401
        else:
            data = {'error': 'User does not exist'}, 401
        db_cursor.close()
        close_connection(conn)

        return data

def register_routes(api):
    api.add_resource(Register, '/register')
    api.add_resource(Login, '/login')