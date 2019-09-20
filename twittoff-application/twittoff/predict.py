"""Prediction of User based on tweet embeddings"""
import numpy as np
from sklearn.linear_model import LogisticRegression
from .db import get_db
import ujson


class AuthorDataModel():
    def __init__(self, author_id, embeddings=None):
        self.author_id = author_id
        self.embeddings = self.fetch_embeddings()

    def __repr__(self):
        return '{}: {} embeddings'.format(self.author_id, self.embeddings.shape())

    def fetch_embeddings(self, number_embeddings=50):
        db = get_db()
        embeddings = []
        embeds_returned = db.execute(
            'SELECT embedding from tweets WHERE author_id = ? LIMIT ?;',
            (self.author_id, number_embeddings)
        ).fetchall()
        for embed in embeds_returned:
            embeddings.append(
                np.array(ujson.loads(embed[0]))
            )

        return np.concatenate(embeddings)


def predict_user(authors, text_to_compare):
    """Determine and return which user is more likely to say a given Tweet."""
    author_space = []
    for author in authors:
        authormodel = AuthorDataModel(author)
        author_space.append(authormodel)

    embeddings = [author.embeddings for author in author_space]
    # stacked_embeddings = np.vstack(embeddings)

    labels = np.concatenate(
        [np.ones(len(author.embeddings))*int(author.author_id) for author in author_space]
        )

    for author in author_space:
       print(author)

    print('stacked len', len(stacked_embeddings))
    print('label_len', len(labels))

    return 'model not available just yet'






    # user1 = User.query.filter(User.name == user1_name).one()
    # user2 = User.query.filter(User.name == user2_name).one()
    # user1_embeddings = np.array([tweet.embedding for tweet in user1.tweets])
    # user2_embeddings = np.array([tweet.embedding for tweet in user2.tweets])
    # embeddings = np.vstack([user1_embeddings, user2_embeddings])
    # labels = np.concatenate([np.ones(len(user1.tweets)),
    #                          np.zeros(len(user2.tweets))])
    # log_reg = LogisticRegression().fit(embeddings, labels)

    # tweet_embedding = BASILICA.embed_sentence(tweet_text, model='twitter')
    #return log_reg.predict(np.array(tweet_embedding).reshape(1, -1))