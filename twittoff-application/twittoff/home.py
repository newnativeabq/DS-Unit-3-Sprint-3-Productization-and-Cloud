from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from twittoff.auth import login_required
from twittoff.db import get_db
from twittoff.twitter import (
    db_add_handle, TweetPackage, update_tweets, get_current_handles
)
from twittoff.forms import AddHandleForm, AnalyzeHandlesForm
from twittoff.predict import predict_user

bp = Blueprint('home', __name__)


# Routes on Home Page


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
        new_handle = request.form['twitter_handle']
        db_add_handle(new_handle)

    return redirect(url_for('home.index'))


@bp.route('/analyze', methods=['POST'])
def analyze_handles():
    if request.method == 'POST':
        selected_handles = request.form.getlist('select_handles')
        update_tweets(selected_handles)
        text_to_compare = request.form['text_to_compare']
        g.mo = run_model(authors=selected_handles, text_to_compare=text_to_compare)

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


# Helper Functions

def get_model_output():
    if 'mo' not in g:
        return 'Model Not Initialized'
    return g.mo


def run_model(authors, text_to_compare):
    return predict_user(authors, text_to_compare)