from tweepy import Stream
from tweepy import OAuthHandler
from libs.twitter_stream import TwitterStream
import os


def scan_twitter(track):

    #consumer key, consumer secret, access token, access secret.
    ckey = os.environ['TWITTER_CONSUMER_KEY']
    csecret = os.environ['TWITTER_CONSUMER_SECRET']
    atoken = os.environ['TWITTER_API_TOKEN']
    asecret = os.environ['TWITTER_API_SECRET']

    auth = OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)

    twitterStream = Stream(auth, TwitterStream())
    twitterStream.filter(track=track)

if __name__ == '__main__':
    scan_twitter(["clayton"])

