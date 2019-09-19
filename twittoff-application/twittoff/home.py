from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from twittoff.auth import login_required
from twittoff.db import get_db
from twittoff.twitter import get_tweets, push_tweets, TweetPackage
from twittoff.forms import AddHandleForm, AnalyzeHandlesForm


bp = Blueprint('home', __name__)


@bp.route('/', methods=('GET', 'POST'))
def index():
    # load forms and form display information
    add_form = AddHandleForm()
    analyze_form = AnalyzeHandlesForm()
    analyze_form.select_handles.choices = get_current_handles()

    # load model_data
    model_output = get_model_output()

    return render_template(
        'index.html',
        addform=add_form,
        analyzeform=analyze_form,
        modeloutput=model_output)


@bp.route('/add', methods=['POST'])
def add_handle():
    if request.method == 'POST':
        db = get_db()
        new_handle = request.form['twitter_handle']
        if db.execute(
            'SELECT id FROM authors WHERE twitter_handle = (?);', (new_handle,)
        ).fetchone() is None:
            db.execute(
                'INSERT INTO authors (twitter_handle) VALUES (?);',
                (new_handle,)
            )
            print('Inserted {} into DB'.format(new_handle))
            db.commit()
            return redirect(url_for('home.index'))
        else:
            flash('Handle Already Entered')
            return redirect(url_for('home.index'))

    return redirect(url_for('home.index'))


@bp.route('/analyze', methods=['POST'])
def analyze_handles():
    if request.method == 'POST':
        selected_handles = request.form.getlist('select_handles')
        print(update_tweets(selected_handles))
        text_to_compare = request.form['text_to_compare']

    return redirect(url_for('home.index'))


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

# example_tweets = get_tweets(user='vincebrandon', number=5)
# print(example_tweets)


def get_model_output():
    if 'model_output' not in g:
        return 'Model Not Initialized'
    return g.model_output


def update_tweets(author_id_list, min_tweets=20):
    # db = get_db()
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
            print('updating with', package)
            push_tweets(package)
            return True
    return False


def get_handle(author_id):
    db = get_db()
    handle = db.execute(
        'SELECT twitter_handle FROM authors WHERE id = ?;', (author_id,)
    ).fetchone()
    return handle[0]


def count_existing_tweets(author_id):
    db = get_db()
    count = db.execute(
        'SELECT COUNT (*) FROM tweets WHERE author_id = ?;', (author_id,)
    ).fetchone()
    print('author {} count is {}'.format(author_id, count[0]))
    return count[0]

