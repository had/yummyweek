from flask_wtf import FlaskForm
from wtforms import HiddenField, SelectMultipleField, SubmitField
from ..meals.meal_list import get_meals

class SelectMealForm(FlaskForm):
    day = HiddenField("day")
    meals = SelectMultipleField("Pick a meal", choices=[(meal.id, meal.name) for meal in get_meals()])
    submit = SubmitField("Confirm")
