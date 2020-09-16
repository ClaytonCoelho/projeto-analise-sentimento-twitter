from flask import Flask
from flask_restful import Api
from libs.api_resource import APIResource
from libs.aws_s3 import AWSS3


app = Flask(__name__)
api = Api(app)

api.add_resource(APIResource, '/predict')


if __name__ == '__main__':
    aws_s3 = AWSS3()
    download_model_data = aws_s3.download_file("model.h5", "twitter-kaggle-data", "data/")
    download_tokenizer_data = aws_s3.download_file("tokenizer.pkl", "twitter-kaggle-data", "data/")
    if download_model_data and download_tokenizer_data:
        print("Download dados de treino com sucesso")
    else:
        print('Download dados de treino com  erro')

    app.run(host='0.0.0.0', port=80)