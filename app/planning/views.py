from flask import jsonify, request, render_template, redirect, url_for, flash

from . import planning

from .forms import SelectMealForm
from datetime import date
import calendar
from .meal_history import get_history, set_history
from .meal_planning import suggest_meals
from ..meals.meal_list import get_meals

weekdays = list(calendar.day_name)
month_names = list(calendar.month_name)


@planning.route("/plans")
def plans():
    now = date.today()
    year = now.year
    month = now.month
    return redirect(url_for(".date_plans", year=year, month=month))

@planning.route("/plans/<int:year>/<int:month>")
def date_plans(year, month):
    mealform = SelectMealForm()
    history = get_history(year, month)
    mealnames = {meal.id:meal.name for meal in get_meals()}
    # previous/next month links
    prev = (year - 1, 12) if month == 1 else (year, month - 1)
    next = (year + 1, 1) if month == 12 else (year, month + 1)
    # calendar related
    cal = calendar.Calendar()
    now = date.today()
    today =  now.day if (now.year == year and now.month == month ) else -1
    return render_template("plans.html", year=year, month=month, monthname=month_names[month],
                           weekdays=weekdays, weeks=cal.monthdayscalendar(year, month), mealform=mealform,
                           history=history, mealnames=mealnames, prev=prev, next=next, today=today)


@planning.route("/plans/<int:year>/<int:month>/add_meal", methods=["POST"])
def add_meal(year, month):
    mealform = SelectMealForm()
    if mealform.validate_on_submit():
        day = int(mealform.day.data)
        set_history(year, month, day, mealform.meals.data)
    else:
        print(mealform.errors.values())
    return redirect(url_for('.date_plans', year=year, month=month))

@planning.route("/plans/<int:year>/<int:month>/meals", methods=["POST"])
def selected_meals(year, month):
    day = int(request.form['day'])
    return jsonify(get_history(year, month)[day])

@planning.route("/suggest")
def suggest():
    now = date.today()
    duration = 7
    meals = get_meals()
    suggestions = suggest_meals(now, duration)
    # suggestions = {
    #     now: [
    #         meals[0],
    #         meals[1]
    #     ]
    # }
    mealnames = {meal.id: meal.name for meal in get_meals()}
    return render_template("suggest.html", start_date=str(now), nb_days=duration, mealnames=mealnames,
                           suggestions=suggestions)