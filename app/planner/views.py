import calendar

from flask import render_template, redirect, url_for
from datetime import date
from . import planner, date_range

from .meal_planning import MealPlanner
from .params import get_params
from .suggestions_dao import get_or_create_suggestions, recreate_suggestion

weekdays = list(calendar.day_name)


@planner.route("/suggest")
def suggest():
    now = date.today()
    duration = 7
    suggestions = get_or_create_suggestions(now, duration)
    suggested_meals = {}
    lunches = suggestions.lunches.split(';')
    dinners = suggestions.dinners.split(';')
    for i, d in enumerate(date_range(now, duration)):
        suggested_meals[d] = [lunches[i], dinners[i]]
    planner = MealPlanner(now)
    # suggestions = {
    #     now: [
    #         meals[0],
    #         meals[1]
    #     ]
    # }
    mealnames = {k: v.name for k, v in planner.meals_dict.items()}
    return render_template("suggest.html", start_date=str(now), nb_days=duration, mealnames=mealnames,
                           suggestions=suggested_meals)


@planner.route("/suggest/redo")
def redo_suggest():
    now = date.today()
    duration = 7
    _ = recreate_suggestion(now, duration)
    return redirect(url_for('.suggest'))


@planner.route("/suggest/params")
def params():
    parameters = get_params()
    print(parameters)
    return render_template("params.html", days=weekdays, parameters=parameters)
