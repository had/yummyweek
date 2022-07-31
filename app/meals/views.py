
from flask import render_template, redirect, url_for, flash


from . import meals
from .meal_list import get_meals



@meals.route("/meals")
def meals():
    return render_template("meals.html", meals=get_meals())
