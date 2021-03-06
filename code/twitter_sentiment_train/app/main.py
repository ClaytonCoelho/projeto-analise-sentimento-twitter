from flask import Flask
from flask_restful import Api
from libs.api_resource import APIResource


app = Flask(__name__)
api = Api(app)

api.add_resource(APIResource, '/train')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)