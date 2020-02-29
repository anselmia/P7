from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired


class EntryForm(FlaskForm):
    entry = TextAreaField("entry", validators=[DataRequired()])
    submit = SubmitField("Ask GrandPy")
