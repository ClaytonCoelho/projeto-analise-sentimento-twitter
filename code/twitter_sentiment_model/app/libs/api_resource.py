from flask_restful import Resource
from flask import jsonify, request
from libs.model import Model

class APIResource(Resource):
    def post(self):
        model = Model()
        text = request.json['text']
        predict = model.predict(text)
        return jsonify(predict)

