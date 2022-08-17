from flask_wtf import FlaskForm
from wtforms import HiddenField, SelectField, SubmitField

class ModifySuggestionForm(FlaskForm):
    date = HiddenField("date")
    suggestion = SelectField("Choose another suggestion", choices=[])
    submit = SubmitField("Confirm")
