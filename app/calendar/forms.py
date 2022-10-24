from flask_wtf import FlaskForm
from wtforms import HiddenField, SelectMultipleField, SubmitField
from ..meals.dao import get_dish_names


class SelectMealForm(FlaskForm):
    day = HiddenField("day")
    remove_suggestions = HiddenField("remove_suggestions")
    meals = SelectMultipleField("Pick a meal", choices=lambda: get_dish_names().items())
    submit = SubmitField("Confirm")
