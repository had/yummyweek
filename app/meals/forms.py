from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import StringField, SelectField, IntegerField, FileField, SubmitField
from wtforms.validators import DataRequired


class MealElementForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    category = SelectField("Category", validators=[DataRequired()])
    prep_time = IntegerField("Preparation time (minutes)", validators=[DataRequired()], default=0)
    cooking_time = IntegerField("Preparation time (minutes)", validators=[DataRequired()], default=0)
    periodicity = IntegerField("Min. days before eating again", validators=[DataRequired()], default=0)


class DishesUploadForm(FlaskForm):
    xlsx_file = FileField(validators=[FileRequired(), FileAllowed(['xlsx'], "Please upload .xlsx files")])
    submit = SubmitField("Upload")
