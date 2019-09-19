from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectMultipleField
from wtforms.validators import DataRequired

from flask import g


class AddHandleForm(FlaskForm):
    twitter_handle = StringField('Handle', validators=[DataRequired()], id='handle')
    submit = SubmitField('Add Handle')


class AnalyzeHandlesForm(FlaskForm):
    text_to_compare = StringField('Text to Compare', validators=[DataRequired], id='text')
    select_handles = SelectMultipleField(label='Handles', id='selected_handles')
    submit = SubmitField('Check Tweets')