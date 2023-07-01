from flask import Flask
from flask_restful import Api
from routes import register_routes
from flask_cors import CORS

app = Flask(__name__) 
api = Api(app)

register_routes(api)

app.debug = True

if __name__ == '__main__':
    app.run()