import calendar

from flask import render_template
from datetime import date
from . import planner

from .meal_planning import suggest_meals
from .params import get_params
from ..meals.meal_list import get_meals

weekdays = list(calendar.day_name)

@planner.route("/suggest")
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

@planner.route("/suggest/params")
def params():
    parameters = get_params()
    print(parameters)
    return render_template("params.html", days=weekdays, parameters=parameters)
