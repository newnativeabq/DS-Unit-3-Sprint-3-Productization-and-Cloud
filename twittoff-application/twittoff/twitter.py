import tweepy
import os

from flask import current_app, g
from flask.cli import with_appcontext


def get_twitter_connection():
    if 'twc' not in g:
        auth = tweepy.OAuthHandler(
            os.environ.get('TWITTER_CONSUMER_KEY'),
            os.environ.get('TWITTER_CONSUMER_SECRET')
        )
        auth.set_access_token(
            os.environ.get('TWITTER_ACCESS_TOKEN'),
            os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
        )
        g.twc = tweepy.API(auth)

    return g.twc


def get_tweets(user, number):
    twc = get_twitter_connection()
    tweets = twc.user_timeline(
        user,
        count=number,
    )
    # strip unnecessary meta tags and return only body text from tweets
    tmp = []
    for tweet in tweets:
        tmp.append(tweet.text)

    return tmp


def push_tweets(user, tweets):
    bsc = None
