import calendar

from flask import render_template, redirect, url_for, jsonify, request
from datetime import date
from . import planner, date_range
from .forms import ModifySuggestionForm

from .meal_planning import MealPlanner
from .models import MealTime
from .params import get_params
from .suggestions_dao import get_or_create_suggestions, recreate_suggestion, get_suggestion, update_suggestion
from ..meals.meal_dao import get_meals, ingredients_for_meals

weekdays = list(calendar.day_name)
weekdays_abbr = list(calendar.day_abbr)


@planner.route("/suggest")
def suggest():
    now = date.today()
    duration = 7
    suggestionform = ModifySuggestionForm()
    suggestions = get_or_create_suggestions(now, duration)
    print([(s.date, s.time, s.suggestion) for s in suggestions])
    lunches = [s.suggestion for s in suggestions[::2]]
    dinners = [s.suggestion for s in suggestions[1::2]]
    planner = MealPlanner(now)
    mealnames = {k: v.name for k, v in planner.meals_dict.items()}
    dates = [(weekdays_abbr[calendar.weekday(d.year, d.month, d.day)], d) for d in date_range(now, duration)]
    return render_template("suggest.html", start_date=str(now), nb_days=duration, mealnames=mealnames,
                           suggestionform=suggestionform, dates=dates,
                           suggested_lunches=lunches, suggested_dinners=dinners)


@planner.route("/suggest/choices", methods=["POST"])
def get_choices():
    mock_data = ["STUFFED_TOMATOES", "RICE_SALAD", "COUSCOUS"]
    form_data = request.form['date'].split("/")
    d = date.fromisoformat(form_data[0])
    lunch_or_dinner = MealTime.lunch if form_data[1] == "L" else MealTime.dinner
    suggestion = get_suggestion(d, lunch_or_dinner)
    meal_dict = get_meals()
    choices = suggestion.eligible_meals.split(";")
    print("GET_CHOICES: ", d, lunch_or_dinner, choices)
    return jsonify({"choices": {m: meal_dict[m].name for m in choices}, "suggestion": suggestion.suggestion})


@planner.route("/suggest/modify", methods=["POST"])
def modify_suggestion():
    suggestionform = ModifySuggestionForm()
    if suggestionform.submit():
        form_data = suggestionform.date.data.split("/")
        d = date.fromisoformat(form_data[0])
        lunch_or_dinner = MealTime.lunch if form_data[1] == "L" else MealTime.dinner
        update_suggestion(d, lunch_or_dinner, suggestionform.suggestion.data)
    else:
        print("### modify_suggestion: ", suggestionform.errors)
    return redirect(url_for(".suggest"))

@planner.route("/suggest/redo")
def redo_suggest():
    now = date.today()
    duration = 7
    _ = recreate_suggestion(now, duration)
    return redirect(url_for('.suggest'))


@planner.route("/suggest/shoppinglist")
def shoppinglist():
    now = date.today()
    duration = 7
    suggestions = get_or_create_suggestions(now, duration)
    ingr_list = ingredients_for_meals([s.suggestion for s in suggestions])
    print(" -*- ", ingr_list)
    return render_template("shoppinglist.html", ingredients=ingr_list)

@planner.route("/suggest/params")
def params():
    parameters = get_params()
    print(parameters)
    return render_template("params.html", days=weekdays, parameters=parameters)

@planner.route("/js/planner-script")
def planner_script():
    return render_template("planner-script.js")