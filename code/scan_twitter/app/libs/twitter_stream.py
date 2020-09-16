
from tweepy.streaming import StreamListener
import json
from libs.dataprep import DataPrep
from libs.sentiment_analysis import SentimentAnalysis
from libs.aws_dynamodb import AWSDynamoDB


class TwitterStream(StreamListener):

    def on_data(self, data):
        data_prep = DataPrep()
        analysis = SentimentAnalysis()
        dynamodb = AWSDynamoDB()

        all_data = json.loads(data)
        text = all_data["text"]
        text_clean = data_prep.clean_text(text)
        sentiment = analysis.analysis(text_clean)

        twitter_sentiment = {
            "id": {"S": all_data["id_str"]},
            "user": {"S": all_data["user"]["screen_name"]},
            "sentiment": {"S": sentiment["label"]},
            "score": {"S": str(sentiment["score"])},
            "twitter_raw": {"S": all_data["text"]},
            "twitter_clean": {"S": text_clean},
            "date": {"S": all_data["created_at"]}
        }

        response = dynamodb.put_item(twitter_sentiment, "twitter_sentiment")


        print(twitter_sentiment)
        return(True)

    def on_error(self, status):
        print(status)

