from flask_wtf import FlaskForm
from wtforms import HiddenField, SelectField, SubmitField, EmailField, validators


class ModifySuggestionForm(FlaskForm):
    date = HiddenField("date")
    suggestion = SelectField("Choose another suggestion", choices=[])
    submit = SubmitField("Confirm")

class EmailForm(FlaskForm):
    email = EmailField('Email address', [validators.DataRequired(), validators.Email()])
    submit = SubmitField("Send")
