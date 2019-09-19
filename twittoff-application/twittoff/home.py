from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort

from twittoff.auth import login_required
from twittoff.db import get_db

from twittoff.twitter import get_twitter_connection

bp = Blueprint('home', __name__)

@bp.route('/', methods=('GET', 'POST'))
def index():
    db = get_db()

    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        pass
        # some val = db.execute(some query)

    return render_template('index.html')
