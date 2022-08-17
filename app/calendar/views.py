from flask import jsonify, request, render_template, redirect, url_for

from . import calendar

from .forms import SelectMealForm
from datetime import date
import calendar as py_cal
from .meal_history import get_history, set_history
from ..meals.meal_dao import get_meals, get_meal_elements

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
    mealform = SelectMealForm()
    history = {d.day:meals for d,meals in get_history(year, month).items()}
    print(history)
    mealnames = {m_id: meal.name for m_id, meal in get_meals().items()}
    mealnames.update({elt.id:elt.name for elt in get_meal_elements()})
    # previous/next month links
    prev = (year - 1, 12) if month == 1 else (year, month - 1)
    next_ = (year + 1, 1) if month == 12 else (year, month + 1)
    # calendar related
    cal = py_cal.Calendar()
    now = date.today()
    today = now.day if (now.year == year and now.month == month ) else -1
    return render_template("calendar.html", year=year, month=month, monthname=month_names[month],
                           weekdays=weekdays, weeks=cal.monthdayscalendar(year, month), mealform=mealform,
                           history=history, mealnames=mealnames, prev=prev, next=next_, today=today)


@calendar.route("/calendar/<int:year>/<int:month>/add_meal", methods=["POST"])
def add_meal(year, month):
    mealform = SelectMealForm()
    if mealform.validate_on_submit():
        day = int(mealform.day.data)
        set_history(year, month, day, mealform.meals.data)
    else:
        print(mealform.errors.values())
    return redirect(url_for('.calendar_month', year=year, month=month))

@calendar.route("/calendar/<int:year>/<int:month>/meals", methods=["POST"])
def selected_meals(year, month):
    day = int(request.form['day'])
    return jsonify(get_history(year, month).get(date(year, month, day)))

@calendar.route("/js/calendar-script/<year>/<month>")
def calendar_script(year, month):
    return render_template("calendar-script.js", year=year, month=month)