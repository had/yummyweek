from flask import render_template
from . import meals
from .meal_dao import get_all_meals


@meals.route("/meals")
def meals():
    return render_template("meals.html", meals=get_all_meals().values())
