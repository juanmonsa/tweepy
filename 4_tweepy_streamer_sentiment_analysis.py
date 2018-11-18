from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

from textblob import TextBlob

import twitter_credential
import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt


# Twitter client
class TwitterClient():
    """
    Client allow you bring an user timeline tweets. If you dont specify any user it defaults to you.
    """
    def __init__(self, twitter_user=None):
        self.auth = TwitterAthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)

        self.twitter_user = twitter_user

    def get_twitter_client_api(self):
        return self.twitter_client
    
    def get_user_timelilne_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_friend_list(self, num_friends):
        friends = []
        for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
            friends.append(friend)
        return friends

    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets


# Twitter Authenticator
class TwitterAthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(twitter_credential.CONSUMER_KEY, twitter_credential.CONSUMER_SECRET)
        auth.set_access_token(twitter_credential.ACCESS_TOKEN, twitter_credential.ACCESS_TOKEN_SECRET)
        return auth


# Twitter Streamer
class TwitterStreamer():
    """
    Class for streaming and processing live tweets.
    """

    def __init__(self):
        self.twitter_authenticator = TwitterAthenticator()

    def stream_tweets(self, fetched_tweets_filename, hashtag_list):

        listener = TwitterListener(fetched_tweets_filename)
        auth = self.twitter_authenticator.authenticate_twitter_app()
        stream = Stream(auth, listener)
        stream.filter(track=hashtag_list)


# Twitter Stream Listener
class TwitterListener(StreamListener):
    """
    Basic listener class that just prints received tweets to stdout.
    """

    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        try:
            print(data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on data: %s" % str(e))
            return True

    def on_error(self, status):
        if status == 420:
            # Return False on_data method in case rate limit occur.
            return False
        print(status)

class TweetAnalyzer():
    """
    Analizyng and categorizing content from tweets.
    """
    def clean_tweet(self, tweet):
       return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def analyze_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))

        if analysis.sentiment.polarity > 0:
            return 1
        elif analysis.sentiment.polarity == 0:
            return 0
        else:
            return -1

    def tweets_to_dataframe(self, tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['tweets'])
        df['id'] = np.array([tweet.id for tweet in tweets])
        df['len'] = np.array([len(tweet.text) for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['source'] = np.array([tweet.source for tweet in tweets])
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])
        return df

    

if __name__ == "__main__":
    twitter_client = TwitterClient()
    tweet_analyzer = TweetAnalyzer()
    api = twitter_client.get_twitter_client_api()

    tweets = api.user_timeline(screen_name="realDonaldTrump", count=200)
    df = tweet_analyzer.tweets_to_dataframe(tweets)

    df['sentiment'] = np.array([tweet_analyzer.analyze_sentiment(tweet) for tweet in df['tweets']])

    print(df.head(10))



