""" Import Section """


from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired


class EntryForm(FlaskForm):
    """ 
        Class that herit from Flaskform
        to set up form information frome home page 
    """
    entry = TextAreaField("entry", validators=[DataRequired()])
    submit = SubmitField("Ask GrandPy")
