import calendar
import os
import smtplib
import ssl

from flask import render_template, redirect, url_for, jsonify, request, current_app
from datetime import date
from . import planner, date_range
from .forms import ModifySuggestionForm, EmailForm

from .meal_planning import MealPlanner
from .models import MealTime, Suggestion
from .params import get_params
from .shopping import get_categorized_shoppinglist
from .suggestions_dao import get_or_create_suggestions, recreate_suggestion, get_suggestion, update_suggestion
from .. import db
from ..meals.meal_dao import get_all_meals

weekdays = list(calendar.day_name)
weekdays_abbr = list(calendar.day_abbr)


@planner.route("/suggest")
def suggest():
    now = date.today()
    duration = 7
    suggestion_form = ModifySuggestionForm()
    suggestions = get_or_create_suggestions(now, duration)
    lunches = [(s.suggestion, s.committed) for s in suggestions[::2]]
    dinners = [(s.suggestion, s.committed) for s in suggestions[1::2]]

    planner = MealPlanner(now)
    mealnames = {k: v.name for k, v in planner.meals_dict.items()}
    prep_times = {k: round(v.prep_time_m) for k, v in planner.meals_dict.items()}
    cooking_times = {k: round(v.cooking_time_m) for k, v in planner.meals_dict.items()}
    dates = [(weekdays_abbr[calendar.weekday(d.year, d.month, d.day)], d) for d in date_range(now, duration)]
    return render_template("suggest.html", start_date=str(now), nb_days=duration, mealnames=mealnames,
                           suggestion_form=suggestion_form, dates=dates,
                           prep_times=prep_times, cooking_times=cooking_times,
                           suggested_lunches=lunches, suggested_dinners=dinners)


@planner.route("/suggest/choices", methods=["POST"])
def get_choices():
    form_data = request.form['date'].split("/")
    d = date.fromisoformat(form_data[0])
    lunch_or_dinner = MealTime.lunch if form_data[1] == "L" else MealTime.dinner
    suggestion = get_suggestion(d, lunch_or_dinner)
    meal_dict = get_all_meals()
    eligible_meals = suggestion.eligible_meals.split(";")
    filtered = {m: meal_dict[m].name for m in eligible_meals}
    other = {m_id: m.name for m_id, m in meal_dict.items() if m_id not in eligible_meals}
    return jsonify({"filtered": filtered, "other": other, "suggestion": suggestion.suggestion})


@planner.route("/suggest/modify", methods=["POST"])
def modify_suggestion():
    suggestion_form = ModifySuggestionForm()
    if suggestion_form.submit():
        form_data = suggestion_form.date.data.split("/")
        d = date.fromisoformat(form_data[0])
        lunch_or_dinner = MealTime.lunch if form_data[1] == "L" else MealTime.dinner
        update_suggestion(d, lunch_or_dinner, suggestion_form.suggestion.data)
    else:
        print("### modify_suggestion: ", suggestion_form.errors)
    return redirect(url_for(".suggest"))


@planner.route("/suggest/commit")
def commit_suggestion():
    d = date.fromisoformat(request.args['date'])
    print(request.args)
    lunch_or_dinner = MealTime.lunch if request.args['time'] == "L" else MealTime.dinner
    print("commit_suggestion: ", d, lunch_or_dinner)
    Suggestion.query.filter_by(date=d, time=lunch_or_dinner).update({Suggestion.committed: True})
    db.session.commit()
    return redirect(url_for(".suggest"))


@planner.route("/suggest/uncommit")
def uncommit_suggestion():
    d = date.fromisoformat(request.args['date'])
    print(request.args)
    lunch_or_dinner = MealTime.lunch if request.args['time'] == "L" else MealTime.dinner
    print("uncommit_suggestion: ", d, lunch_or_dinner)
    Suggestion.query.filter_by(date=d, time=lunch_or_dinner).update({Suggestion.committed: False})
    db.session.commit()
    return redirect(url_for(".suggest"))


@planner.route("/suggest/redo")
def redo_suggest():
    now = date.today()
    duration = 7
    sugg = recreate_suggestion(now, duration)
    print("RECREATE_SUGG ", [(s.date, s.time, s.suggestion) for s in sugg])
    return redirect(url_for('.suggest'))


@planner.route("/suggest/shoppinglist")
def shoppinglist():
    email_form = EmailForm()
    now = date.today()
    duration = 7
    ingredients_grouped = get_categorized_shoppinglist(now, duration)
    return render_template("shoppinglist.html", ingredients_grouped=ingredients_grouped, email_form=email_form)


@planner.route("/suggest/shoppinglist/send", methods=["POST"])
def send_shoppinglist():
    email_form = EmailForm()
    if email_form.validate_on_submit():
        print("Will send email to ", email_form.email.data)

        context = ssl.create_default_context()
        smtp_srv = current_app.config['SMTP_SERVER']
        smtp_port = current_app.config['SMTP_PORT']
        yw_email = os.environ.get("YW_EMAIL")
        yw_email_pw = os.environ.get("YW_EMAIL_PW")
        now = date.today()
        duration = 7
        ingredients_grouped = get_categorized_shoppinglist(now, duration)
        msg = render_template("ingredients_by_category.html", ingredients_grouped=ingredients_grouped)
        print("Sending the following message:")
        print(msg)
        with smtplib.SMTP_SSL(smtp_srv, smtp_port, context=context) as server:
            server.login(yw_email, yw_email_pw)
            server.sendmail(yw_email, email_form.email.data, msg=msg)
    return redirect(url_for('.shoppinglist'))


@planner.route("/suggest/params")
def params():
    parameters = get_params()
    print(parameters)
    return render_template("params.html", days=weekdays, parameters=parameters)


@planner.route("/js/planner-script")
def planner_script():
    return render_template("planner-script.js")
