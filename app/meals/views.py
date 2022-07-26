
from flask import render_template, redirect, url_for, flash


from . import meals, mock_meals



@meals.route("/meals")
def meals():
    return render_template("meals.html", meals=mock_meals)
