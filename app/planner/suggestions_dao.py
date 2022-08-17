from datetime import timedelta

from sqlalchemy import and_

from . import date_range
from .models import Suggestion, MealTime
from .. import db
from .meal_planning import MealPlanner, suggest_meal


def get_suggestion(date_, time_):
    return Suggestion.query.filter(and_(Suggestion.date == date_, Suggestion.time == time_)).one()


def get_or_create_suggestions(from_date, duration):
    suggestions_res = Suggestion.query.filter(Suggestion.date >= from_date).all()
    retrieved_days = len(suggestions_res)//2
    if retrieved_days >= duration:
        # we retrieved everything we want from DB, we're done here ...
        return suggestions_res[:duration*2]

    # ... otherwise, we have a partial result from DB. We must complete that with new suggestions.
    # replay the suggestions retrieved: prepare a planner, feed it the suggestions retrieved (if any)
    planner = MealPlanner(from_date)
    sugg_dates = date_range(from_date, retrieved_days)
    sugg_iter = iter([s.suggestion for s in suggestions_res])
    # the following zip takes suggestions 2 by 2 (to take lunch and dinner together), see the Tips and tricks paragraph
    # of https://docs.python.org/3/library/functions.html#zip
    for d, lunch, dinner in zip(sugg_dates, sugg_iter, sugg_iter):
        planner.process_dated_meals(d, [lunch, dinner])
    # for the rest of the duration, we ask for suggestions
    for d in date_range(from_date + timedelta(days=retrieved_days), duration-retrieved_days):
        for t in MealTime:
            eligible, suggested_m_id = suggest_meal(d, t, planner)
            planner.process_dated_meals(d, [suggested_m_id])
            suggestion = Suggestion(date=d, time=t, eligible_meals=";".join([m.id for m in eligible]), suggestion=suggested_m_id)
            suggestions_res.append(suggestion)
            db.session.add(suggestion)
    db.session.commit()
    return suggestions_res

def recreate_suggestion(from_date, duration):
    Suggestion.query.filter(Suggestion.date >= from_date).delete()
    return get_or_create_suggestions(from_date, duration)
