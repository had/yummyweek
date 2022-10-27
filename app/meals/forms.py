from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import StringField, SelectField, IntegerField, FileField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired


class DishForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    prep_time = IntegerField("Preparation time (minutes)", validators=[DataRequired()], default=0)
    cooking_time = IntegerField("Preparation time (minutes)", validators=[DataRequired()], default=0)
    periodicity = IntegerField("Min. days before eating again", validators=[DataRequired()], default=0)
    moment = SelectField("Moment", validators=[DataRequired()], choices=["-", "Lunch", "Dinner", "Both"])
    elements = SelectMultipleField("Elements", choices=[])
    submit = SubmitField("Add")


class DishesUploadForm(FlaskForm):
    xlsx_file = FileField(validators=[FileRequired(), FileAllowed(['xlsx'], "Please upload .xlsx files")])
    submit = SubmitField("Upload")
