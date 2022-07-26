from flask_wtf import FlaskForm
from wtforms import HiddenField, SelectMultipleField, SubmitField
from ..meals import mock_meals

class SelectMealForm(FlaskForm):
    day = HiddenField("day")
    meals = SelectMultipleField("Pick a meal", coerce=int, choices=[(meal.id, meal.name) for meal in mock_meals])
    submit = SubmitField("Confirm")
