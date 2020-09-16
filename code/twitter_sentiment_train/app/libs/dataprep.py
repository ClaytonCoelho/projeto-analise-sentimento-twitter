import pandas as pd
import re

# nltk
import nltk
from nltk.corpus import stopwords
from  nltk.stem import SnowballStemmer



class DataPrep:
    def __init__(self):
        nltk.download('stopwords')
        self.path_data = "data/training.1600000.processed.noemoticon.csv"
        self.dataset_columns = ["target", "ids", "date", "flag", "user", "text"]
        self.dataset_encoding = "ISO-8859-1"
        self.decode_map = {0: "NEGATIVE", 2: "NEUTRAL", 4: "POSITIVE"}
        self.text_cleaning_re = "@\S+|https?:\S+|http?:\S|[^A-Za-z0-9]+"
        self.stop_words = stopwords.words("english")
        self.stemmer = SnowballStemmer("english")

    
    def __decode_sentiment(self, label):
        return self.decode_map[int(label)]

    def __clean_text(self, text, stem=False):
        # Remove link,user and special characters
        text = re.sub(self.text_cleaning_re, ' ', str(text).lower()).strip()
        tokens = []
        for token in text.split():
            if token not in self.stop_words:
                if stem:
                    tokens.append(self.stemmer.stem(token))
                else:
                    tokens.append(token)
        return " ".join(tokens)

    def import_data_train(self):
        df = pd.read_csv(self.path_data, encoding=self.dataset_encoding, names=self.dataset_columns)
        df.target = df.target.apply(lambda x: self.__decode_sentiment(x))
        df.text = df.text.apply(lambda x: self.__clean_text(x))
        return df
