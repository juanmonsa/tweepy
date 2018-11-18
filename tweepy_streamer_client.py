from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import twitter_credential

# Twitter client
class TwitterClient():
    """
    Client allow you bring an user timeline tweets. If you dont specify any user it defaults to you.
    """
    def __init__(self, twitter_user=None):
        self.auth = TwitterAthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)

        self.twitter_user = twitter_user
    
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
        for home_tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(home_tweet)
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


if __name__ == "__main__":

    twitter_client = TwitterClient('pycon')
    print(twitter_client.get_user_timelilne_tweets(1))
    #print(twitter_client.get_home_timeline_tweets(1))
    #print(twitter_client.get_friend_list(1))
 


# CTRL+ALT+N : Will print tweets from an user timeline, tweets from home timelie and friend list





