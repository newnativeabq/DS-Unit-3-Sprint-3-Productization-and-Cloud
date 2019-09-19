from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from twittoff.auth import login_required
from twittoff.db import get_db
from twittoff.twitter import get_tweets
from twittoff.forms import AddHandleForm, AnalyzeHandlesForm


bp = Blueprint('home', __name__)


@bp.route('/', methods=('GET', 'POST'))
def index():
    add_form = AddHandleForm()
    analyze_form = AnalyzeHandlesForm()

    analyze_form.select_handles.choices = get_current_handles()

    return render_template(
        'index.html',
        addform=add_form,
        analyzeform=analyze_form)


@bp.route('/add', methods=['POST'])
def add_handle():
    add_form = AddHandleForm()
    analyze_form = AnalyzeHandlesForm()

    analyze_form.select_handles.choices = get_current_handles()

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

    return render_template(
        'index.html',
        addform=add_form,
        analyzeform=analyze_form)


@bp.route('/analyze', methods=['POST'])
def analyze_handles():
    add_form = AddHandleForm()
    analyze_form = AnalyzeHandlesForm()

    analyze_form.select_handles.choices = get_current_handles()

    return render_template(
        'index.html',
        addform=add_form,
        analyzeform=analyze_form)


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
        print('default_choices', default_choices)
        return default_choices
    print('choices', choices)
    return choices

# example_tweets = get_tweets(user='vincebrandon', number=5)
# print(example_tweets)