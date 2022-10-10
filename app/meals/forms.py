from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField
from wtforms.validators import DataRequired


class MealElementForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    category = SelectField("Category", validators=[DataRequired()])
    prep_time = IntegerField("Preparation time (minutes)", validators=[DataRequired()], default=0)
    cooking_time = IntegerField("Preparation time (minutes)", validators=[DataRequired()], default=0)
    periodicity = IntegerField("Min. days before eating again", validators=[DataRequired()], default=0)

