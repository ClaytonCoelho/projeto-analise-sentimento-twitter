from flask_restful import Resource
from flask import jsonify
from libs.dataprep import DataPrep
from libs.model_train import ModelTrain
from libs.aws_s3 import AWSS3
import pickle

class APIResource(Resource):
    def get(self):
        test = True

        if test:
            result = {"status": "OK"}
        
        else:
            data_prep = DataPrep()
            model_train = ModelTrain()
            aws_s3 = AWSS3()
            download_data_train = aws_s3.download_file("training.1600000.processed.noemoticon.csv", "twitter-kaggle-data", "data/")
            if download_data_train:
                print("Download dados de treino com sucesso")
            else:
                print('Download dados de treino com  erro')



            df = data_prep.import_data_train()

            df_train, df_test = model_train.split_train_test(df)

            w2v_model = model_train.model_w2v(df_train)

            tokenizer_text = model_train.tokenizer_text(df_train)

            x_train, x_test = model_train.x_train_test(tokenizer_text, df_train, df_test)

            encoder = model_train.label_encoder(df_train)

            y_train, y_test = model_train.y_train_test(encoder, df_train, df_test)

            embedding_layer = model_train.embedding_layer(tokenizer_text, w2v_model)

            keras_model = model_train.fit_model(embedding_layer, x_train, y_train)

            keras_model.save("data/model.h5")
            pickle.dump(tokenizer_text, open("data/tokenizer.pkl", "wb"), protocol=0)

            upload_model = aws_s3.upload_file("model.h5", "twitter-kaggle-data", "data/")
            if upload_model:
                print("Upload do modelo com sucesso")
            else:
                print('Upload do modelo com  erro')

            upload_tokenizer = aws_s3.upload_file("tokenizer.pkl", "twitter-kaggle-data", "data/")
            if upload_tokenizer:
                print("Upload do tokenizer com sucesso")
            else:
                print('Upload do tokenizer com  erro')


            result = {"status": "OK"}

        return jsonify(result)




    
