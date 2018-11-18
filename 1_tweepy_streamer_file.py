from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import twitter_credential

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


if __name__ == "__main__":

    hashtag_list = ["donald trump", "hillary clinton"]
    fetched_tweets_filename = "tweets.json"

    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(fetched_tweets_filename, hashtag_list)
 


# CTRL+ALT+N : Will print on a file the tweets streamed





