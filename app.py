from flask import Flask
from flask_restful import Api
from routes import register_routes
from flask_jwt_extended import JWTManager
import config

app = Flask(__name__) 
api = Api(app)
jwt = JWTManager(app)

app.config['JWT_SECRET_KEY'] = config.JWT_SECRET_KEY

register_routes(api)

app.debug = True

if __name__ == '__main__':
    app.run()