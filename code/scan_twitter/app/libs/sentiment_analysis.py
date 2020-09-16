import requests

class SentimentAnalysis:
    def __init__(self):
        self.url_model = "http://twitter-sentiment/predict"
        self.headers = {
            'Content-Type': "application/json"
        }
    
    def analysis(self, text):
        body = {
            "text": text
        }
        response = requests.post(self.url_model, json=body, headers=self.headers)
        data = response.json()

        return data
