from itertools import groupby

from flask import jsonify, request, render_template, redirect, url_for

from . import calendar

from .forms import SelectMealForm
from datetime import date
import calendar as py_cal
from .meal_history import get_history, set_history
from ..meals.meal_dao import get_meals, get_meal_elements
from ..planner.suggestions_dao import get_suggestions, get_committed_suggestions, remove_suggestions

weekdays = list(py_cal.day_name)
month_names = list(py_cal.month_name)


@calendar.route("/calendar")
def calendar_today():
    now = date.today()
    year = now.year
    month = now.month
    return redirect(url_for(".calendar_month", year=year, month=month))

@calendar.route("/calendar/<int:year>/<int:month>")
def calendar_month(year, month):
    meal_form = SelectMealForm()
    # retrieve history and suggestions
    history = {d.day:meals for d,meals in get_history(year, month).items()}
    _, month_duration = py_cal.monthrange(year, month)
    raw_suggestions = get_suggestions(date(year, month, 1), date(year, month, month_duration))
    suggestions = {date_.day:[s.suggestion for s in s_group if s.committed]
                   for date_, s_group in groupby(raw_suggestions, key=lambda s: s.date)}
    # get meal names mapping
    meal_names = {m_id: meal.name for m_id, meal in get_meals().items()}
    meal_names.update({elt.id:elt.name for elt in get_meal_elements()})
    # previous/next month links
    prev = (year - 1, 12) if month == 1 else (year, month - 1)
    next_ = (year + 1, 1) if month == 12 else (year, month + 1)
    # calendar related
    cal = py_cal.Calendar()
    now = date.today()
    today = now.day if (now.year == year and now.month == month ) else -1
    return render_template("calendar.html", year=year, month=month, monthname=month_names[month],
                           weekdays=weekdays, weeks=cal.monthdayscalendar(year, month), mealform=meal_form,
                           history=history, suggestions=suggestions, mealnames=meal_names,
                           prev=prev, next=next_, today=today)


@calendar.route("/calendar/<int:year>/<int:month>/add_meal", methods=["POST"])
def add_meal(year, month):
    mealform = SelectMealForm()
    if mealform.validate_on_submit():
        day = int(mealform.day.data)
        set_history(year, month, day, mealform.meals.data)
        if mealform.remove_suggestions.data:
            remove_suggestions(date(year, month, day))
    else:
        print("### add_meal: ", mealform.errors.values())
    return redirect(url_for('.calendar_month', year=year, month=month))

@calendar.route("/calendar/<int:year>/<int:month>/meals", methods=["POST"])
def selected_meals(year, month):
    day = int(request.form['day'])
    return jsonify(get_history(year, month).get(date(year, month, day)))

@calendar.route("/calendar/<int:year>/<int:month>/suggestion", methods=["POST"])
def suggested_meals(year, month):
    day = int(request.form['day'])
    d = date(year, month, day)
    meal_names = {m_id: meal.name for m_id, meal in get_meals().items()}
    sugg = {s.suggestion: meal_names[s.suggestion] for s in get_committed_suggestions(d)}
    return jsonify(sugg)

@calendar.route("/js/calendar-script/<year>/<month>")
def calendar_script(year, month):
    return render_template("calendar-script.js", year=year, month=month)