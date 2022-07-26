from flask import render_template, redirect, url_for, flash

from . import planning

from .forms import SelectMealForm
from datetime import datetime
import calendar
from .meal_history import get_history, set_history
from ..meals import mock_meals

weekdays = list(calendar.day_name)
month_names = list(calendar.month_name)


@planning.route("/plans")
def plans():
    now = datetime.now()
    year = now.year
    month = now.month
    cal = calendar.Calendar()
    mealform = SelectMealForm()
    history = get_history(year, month)
    mealnames = {meal.id:meal.name for meal in mock_meals}
    return render_template("plans.html", year=year, month=month, monthname=month_names[month],
                           weekdays=weekdays, weeks=cal.monthdayscalendar(year, month), mealform=mealform,
                           history=history, mealnames=mealnames)


@planning.route("/plans/<int:year>/<int:month>/add_meal", methods=["POST"])
def add_meal(year, month):
    mealform = SelectMealForm()
    if mealform.validate_on_submit():
        day = int(mealform.day.data)
        print(day)
        set_history(year, month, day, mealform.meals.data)
        print("SUCCESS: ", get_history(year, month))
    else:
        print(mealform.errors.values())
    return redirect(url_for('.plans'))
