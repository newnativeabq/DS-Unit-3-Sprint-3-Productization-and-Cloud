import tweepy
import os

from flask import current_app, g
from flask.cli import with_appcontext
from twittoff.db import get_db


class TweetPackage():
    def __init__(self, author_id, tweets):
        self.author_id = author_id
        self.tweets = tweets

    def __repr__(self):
        return self.author_id + str(self.tweets)


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


def push_tweets(tweet_packages):
    db = get_db()
    if type(tweet_packages) == list:
        for package in tweet_packages:
            for tweet in package.tweets:
                db.execute(
                    'INSERT INTO tweets (author_id, body) VALUES (?, ?);',
                    (package.author_id, tweet)
                )
    else:
        for tweet in tweet_packages.tweets:
            db.execute(
                'INSERT INTO tweets (author_id, body) VALUES (?, ?);',
                (tweet_packages.author_id, tweet)
            )
    db.commit()
    return True

