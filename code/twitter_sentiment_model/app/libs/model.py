# Keras
from keras.preprocessing.sequence import pad_sequences
from keras.models import load_model

# Utilidades
import pickle

class Model:
    def __init__(self) -> None:
        self.sentiment_thresholds = (0.4, 0.7)
        with open("data/tokenizer.pkl", 'rb') as handle:
            self.tokenizer = pickle.load(handle)
        self.loaded_model = load_model("data/model.h5")
        self.sequence_length = 300

    def __decode_sentiment(self, score, include_neutral) -> str:
        if include_neutral:        
            label = "NEUTRAL"
            if score <= self.sentiment_thresholds[0]:
                label = "NEGATIVE"
            elif score >= self.sentiment_thresholds[1]:
                label = "POSITIVE"

            return label
        else:
            return "NEGATIVE" if score < 0.5 else "POSITIVE"

    def predict(self, text, include_neutral=True) -> dict:
        # Tokenize text
        x_test = pad_sequences(self.tokenizer.texts_to_sequences([text]), maxlen=self.sequence_length)
        # Predict
        score = self.loaded_model.predict([x_test])[0]
        # Decode sentiment
        label = self.__decode_sentiment(score, include_neutral=include_neutral)

        return {"label": label, 
                "score": float(score)}
