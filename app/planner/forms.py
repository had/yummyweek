from flask_wtf import FlaskForm
from wtforms import HiddenField, SelectMultipleField, SubmitField

class ModifySuggestionForm(FlaskForm):
    date = HiddenField("date")
    suggestion = SelectMultipleField("Choose another suggestion", choices=[])
    submit = SubmitField("Confirm")
