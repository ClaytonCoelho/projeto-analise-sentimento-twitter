# Scikit-learn
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Word2vec
import gensim

# Keras
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.layers import Dense, Dropout, Embedding, LSTM
from keras.models import Sequential
from keras.callbacks import ReduceLROnPlateau, EarlyStopping

# Utility
import numpy as np


class ModelTrain:
    def __init__(self):
        self.train_size = 0.8
        self.w2v_size = 300
        self.w2v_window = 7
        self.min_count = 10
        self.w2v_epoch = 32
        self.sequence_length = 300
        self.batch_size = 1024
        self.epochs = 8

    def split_train_test(self, df):
        df_train, df_test = train_test_split(df, test_size=1-self.train_size, random_state=42)

        return df_train, df_test
    
    def model_w2v(self, df_train):
        documents = [_text.split() for _text in df_train.text] 

        w2v_model = gensim.models.word2vec.Word2Vec(size=self.w2v_size, 
                                                    window=self.w2v_window, 
                                                    min_count=self.min_count, 
                                                    workers=8)

        w2v_model.build_vocab(documents)

        w2v_model.train(documents, total_examples=len(documents), epochs=self.w2v_epoch)

        return w2v_model

    def tokenizer_text(self, df_train):
        tokenizer = Tokenizer()
        tokenizer.fit_on_texts(df_train.text)

        return tokenizer

    def x_train_test(self, text_tokenizer, df_train, df_test):
        x_train = pad_sequences(text_tokenizer.texts_to_sequences(df_train.text), maxlen=self.sequence_length)
        x_test = pad_sequences(text_tokenizer.texts_to_sequences(df_test.text), maxlen=self.sequence_length)

        return x_train, x_test

    def label_encoder(self, df_train):
        labels = df_train.target.unique().tolist()
        labels.append("NEUTRAL")

        encoder = LabelEncoder()
        encoder.fit(df_train.target.tolist())

        return encoder
    
    def y_train_test(self, encoder_train, df_train, df_test):
        y_train = encoder_train.transform(df_train.target.tolist())
        y_test = encoder_train.transform(df_test.target.tolist())

        y_train = y_train.reshape(-1,1)
        y_test = y_test.reshape(-1,1)

        return y_train, y_test

    def embedding_layer(self, text_tokenizer, w2v_model):
        vocab_size = len(text_tokenizer.word_index) + 1
        embedding_matrix = np.zeros((vocab_size, self.w2v_size))
        for word, i in text_tokenizer.word_index.items():
            if word in w2v_model.wv:
                embedding_matrix[i] = w2v_model.wv[word]

        embedding_layer = Embedding(vocab_size, self.w2v_size, weights=[embedding_matrix], input_length=self.sequence_length, trainable=False)

        return embedding_layer

    def fit_model(self, embedding_layer, x_train, y_train):
        # Build Model
        model = Sequential()
        model.add(embedding_layer)
        model.add(Dropout(0.5))
        model.add(LSTM(100, dropout=0.2, recurrent_dropout=0.2))
        model.add(Dense(1, activation='sigmoid'))

        # Compile model
        model.compile(loss='binary_crossentropy',
                    optimizer="adam",
                    metrics=['accuracy'])

        # Callbacks
        callbacks = [ ReduceLROnPlateau(monitor='val_loss', patience=5, cooldown=0),
                    EarlyStopping(monitor='val_acc', min_delta=1e-4, patience=5)]

        # Train
        model.fit(x_train, y_train,
                batch_size=self.batch_size,
                epochs=self.epochs,
                validation_split=0.1,
                verbose=1,
                callbacks=callbacks)

        return model
