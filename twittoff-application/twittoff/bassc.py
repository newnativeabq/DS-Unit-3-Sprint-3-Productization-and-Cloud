import basilica
import os
import ujson

from flask import Flask, current_app, g
from twittoff.db import get_db
from werkzeug.local import LocalProxy

app = Flask(__name__)

def get_basilica_connection():
    if 'bsc' not in g:
        g.bsc = basilica.Connection(
            os.environ.get('BASILICA_ACCESS_TOKEN')
        )

    return g.bsc


def get_embeddings(tweet_text):
    print('getting embeddings')
    with app.app_context():
        bsc = get_basilica_connection()
    embedding = bsc.embed_sentence(
                                    tweet_text,
                                    model='twitter',
                                    version='default',
                                    timeout=5,
                                    )
    # format embedding
    print('transforming to json')
    return ujson.dumps(list(embedding))
