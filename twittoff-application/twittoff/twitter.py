import tweepy
import os
from threading import Thread, Event
from queue import Queue

from flask import current_app, g, flash, redirect, url_for
from flask.cli import with_appcontext
from twittoff.db import get_db
from .bassc import get_embeddings


class TweetPackage():
    def __init__(self, author_id, tweets):
        self.id = id
        self.author_id = author_id
        self.tweets = tweets

    def __repr__(self):
        return self.author_id + str(len(self.tweets)) + ' tweets'


class Tweet():
    def __init__(self, tweet_id, full_text, embedding=None):
        self.tweet_id = tweet_id
        self.full_text = full_text
        self.embedding = get_embeddings(full_text)


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
        g.twc = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    return g.twc


def get_tweets(user, number):
    twc = get_twitter_connection()
    print('attemtping to get {} tweets'.format(number))
    tweets = tweepy.Cursor(
        twc.user_timeline, id=user,
         exclude_replies=True,
         include_rts=False,
         tweet_mode='extended',
         ).items(number)

    return process_tweets(tweets)


# multithreaded append to help speed up embedding search and json dump
def process_tweets(tweets):
    num_threads = 3

    def assemble_tweets():
        while True:
            if not queue_in.empty():
                print('building tweet')
                params = queue_in.get()
                queue_out.put(
                    Tweet(params[0], params[1])
                )
            else:
                break

    def queue_to_list(queue_obj):
        return_list = []
        while True:
            if not queue_obj.empty():
                print('appending finished embed')
                return_list.append(queue_obj.get())
            else:
                break
        return return_list

    queue_in = Queue()
    queue_out = Queue()
    for tweet in tweets:
        queue_in.put((tweet.id, tweet.full_text))

    # Spawn worker threads
    tweet_assembler_threads = []
    for _ in range(num_threads):
        t = Thread(target=assemble_tweets)
        t.start()
        tweet_assembler_threads.append(t)
    # Add stop points for each thread
    # for _ in range(num_threads):
    #     queue_in.put(None)
    # Wait for tweets to complete
    for t in tweet_assembler_threads:
        t.join()

    return queue_to_list(queue_out)


def push_tweets(tweet_packages):
    db = get_db()
    print('pushing tweets to db')
    if type(tweet_packages) == list:
        for package in tweet_packages:
            for tweet in package.tweets:
                insert_tweet(author_id=package.author_id, tweet=tweet)
    else:
        for tweet in tweet_packages.tweets:
            insert_tweet(author_id=tweet_packages.author_id, tweet=tweet)
    print('committing changes')
    db.commit()
    return True


def insert_tweet(author_id, tweet):
    # insert tweet object into database
    db = get_db()
    db.execute(
        'INSERT INTO tweets (tweet_id, author_id, body, embedding) VALUES (?, ?, ?, ?);',
        (tweet.tweet_id, author_id, tweet.full_text, tweet.embedding)
    )


def update_tweets(author_id_list, min_tweets=100):
    for author_id in author_id_list:
        if count_existing_tweets(author_id) < min_tweets:
            print('attempting update')
            package = TweetPackage(
                author_id=author_id,
                tweets=get_tweets(
                    user=get_handle(author_id),
                    number=min_tweets
                )
            )
            push_tweets(package)


def count_existing_tweets(author_id):
    db = get_db()
    count = db.execute(
        'SELECT COUNT (*) FROM tweets WHERE author_id = ?;', (author_id,)
    ).fetchone()
    return count[0]


def get_current_handles():
    db = get_db()
    default_choices = [
        ('0', 'vincebrandon'),
        ('1', 'JustinTrudeau'),
        ('2', 'DonaldTrump')
    ]
    choices = db.execute(
        'SELECT * FROM authors;'
    ).fetchall()

    if len(choices) < 1:

        return default_choices
    return choices


def db_add_handle(handle):
    db = get_db()
    if db.execute(
        'SELECT id FROM authors WHERE twitter_handle = (?);', (handle,)
    ).fetchone() is None:
        db.execute(
            'INSERT INTO authors (twitter_handle) VALUES (?);',
            (handle,)
        )
        print('Inserted {} into DB'.format(handle))
        db.commit()
        return redirect(url_for('home.index'))
    else:
        flash('Handle Already Entered')
        return redirect(url_for('home.index'))


def get_handle(author_id):
    db = get_db()
    handle = db.execute(
        'SELECT twitter_handle FROM authors WHERE id = ?;', (author_id,)
    ).fetchone()
    return handle[0]