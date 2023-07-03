from flask_restful import Resource, reqparse
from flask import request
import bcrypt
from datetime import datetime
from utils import validate_email, connect_to_db, log_connection
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required, get_jwt

class Register(Resource):
    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('first_name', required=True)
        parser.add_argument('last_name', required=True)
        parser.add_argument('username', required=True)
        parser.add_argument('email_address', required=True)
        parser.add_argument('role', required=True)
        parser.add_argument('password', required=True)

        args = parser.parse_args()
        first_name = args['first_name']
        last_name = args['last_name']
        username = args['username']
        email_address = args['email_address']
        role = args['role']
        password = args['password']

        if not validate_email(email_address):
            return {'error': 'Invalid email address'}, 400

        hashed_password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        
        query = 'INSERT INTO users (first_name, last_name, username, email, role, password) VALUES (?, ?, ?, ?, ?, ?)'
        params = (first_name, last_name, username, email_address, role, hashed_password)
        connect_to_db(query, fetchall=False, insert=True, params=params)
        log_connection(request)

        return {'message': 'User {} was created successfully'.format(username)}, 201

class Login(Resource):
    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('username', required=True)
        parser.add_argument('password', required=True) 

        args = parser.parse_args()
        username = args['username']
        password = args['password']
        
        query = 'SELECT id, username, password, email, role FROM users WHERE username = ?'
        params = (username,)
        user = connect_to_db(query, fetchall=False, params=params)

        if user:
            stored_hash = user[2]
            if bcrypt.checkpw(password.encode('utf8'), stored_hash):
                access_token = create_access_token(identity=user[1], additional_claims={'username': user[3], 'role': user[4]})
                data = {'access_token': access_token}, 200
            else:
                data = {'error': 'Invalid credentials'}, 401
        else:
            data = {'error': 'User does not exist'}, 401

        log_connection(request)
        return data
    
class Home(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        claims = get_jwt()
        user_role = claims['role']
        
        if current_user:
            data = {
                "message": f"Welcome back {current_user}! Your current role is {user_role}. Great to have you back."
            }, 200
        else:
            data = {
                "message": "Welcome to the home page. You are not registered on the website."
            }, 200
        log_connection(request)
        return data
    
class Log(Resource):
    @jwt_required()
    def get(self):
        claims = get_jwt()
        log_connection(request)
        if claims['role'] != 'Admin':
            return {'message': 'Unauthorized access. Go back to Register Page to register'}, 401
        
        query = 'SELECT ip, connection_date, http_verb, endpoint FROM connections ORDER BY connection_date DESC LIMIT 25'
        latest_connections = connect_to_db(query, fetchall=True)

        query = 'SELECT ip, connection_date, http_verb, endpoint FROM connections'
        all_connections = connect_to_db(query, fetchall=True)

        formatted_latest_connections = []
        formatted_all_connections = []
        date_format = "%b %d, %Y"
        for connection in latest_connections:
            formatted_latest_connections.append({
                'ip': connection[0],
                'date': datetime.strptime(connection[1], date_format).strftime(date_format),
                'http_verb': connection[2],
                'endpoint': connection[3]
            })

        for connection in all_connections:
            formatted_all_connections.append({
                'ip': connection[0],
                'date': datetime.strptime(connection[1], date_format).strftime(date_format),
                'http_verb': connection[2],
                'endpoint': connection[3]
            })

        return {
            'latest_connections': formatted_latest_connections,
            'all_connections': formatted_all_connections
        }, 200


        

def register_routes(api):
    api.add_resource(Register, '/register')
    api.add_resource(Login, '/login')
    api.add_resource(Home, '/home')
    api.add_resource(Log, '/log')