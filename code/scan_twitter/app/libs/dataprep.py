# nltk
import nltk
from nltk.corpus import stopwords
from  nltk.stem import SnowballStemmer

import re

class DataPrep:
    def __init__(self):
        nltk.download('stopwords')
        self.text_cleaning_re = "@\S+|https?:\S+|http?:\S|[^A-Za-z0-9]+"
        self.stop_words = stopwords.words("english")
        self.stemmer = SnowballStemmer("english")

    def __remove_emojis(self, string):
        return string.encode('ascii', 'ignore').decode('ascii')
    
    def clean_text(self, text, stem=False):
        filter_emojis = self.__remove_emojis(text)
        # Remove link,user and special characters
        text_clean = re.sub(self.text_cleaning_re, ' ', str(filter_emojis).lower()).strip()
        tokens = []
        for token in text_clean.split():
            if token not in self.stop_words:
                if stem:
                    tokens.append(self.stemmer.stem(token))
                else:
                    tokens.append(token)
        return " ".join(tokens)
