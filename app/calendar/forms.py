from flask_wtf import FlaskForm
from wtforms import HiddenField, SelectMultipleField, SubmitField
from ..meals.meal_dao import get_meals


class SelectMealForm(FlaskForm):
    day = HiddenField("day")
    remove_suggestions = HiddenField("remove_suggestions")
    meals = SelectMultipleField("Pick a meal", choices=[(m_id, m.name) for m_id, m in get_meals().items()])
    submit = SubmitField("Confirm")
