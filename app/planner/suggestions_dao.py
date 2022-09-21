from datetime import timedelta
from itertools import product

from sqlalchemy import and_, or_

from . import date_range
from .models import Suggestion, MealTime
from .. import db
from .meal_planning import MealPlanner, suggest_meal


def get_suggestion(date_, time_):
    return Suggestion.query.filter(and_(Suggestion.date == date_, Suggestion.time == time_)).one()


def get_suggestions(from_date, to_date):
    return Suggestion.query.filter(Suggestion.date.between(from_date, to_date)).all()

def get_committed_suggestions(date_):
    return [s for s in get_suggestions(date_, date_) if s.committed]

def get_or_create_suggestions(from_date, duration):
    to_date = from_date + timedelta(days=duration)
    suggestions_res = get_suggestions(from_date, to_date)

    # ... otherwise, we have a partial result from DB. We must complete that with new suggestions.
    # replay the suggestions retrieved: prepare a planner, feed it the suggestions retrieved (if any)
    sugg_dict = {(s.date,s.time): s for s in suggestions_res}
    result = []
    planner = MealPlanner(from_date)
    for date_, time_ in product(date_range(from_date, duration+1), [MealTime.lunch, MealTime.dinner]):
        if (date_, time_) in sugg_dict:
            s = sugg_dict[(date_,time_)]
            planner.process_dated_meals(date_, [s.suggestion])
            result.append(s)
        else:
            eligible, suggested_m_id = suggest_meal(date_, time_, planner)
            planner.process_dated_meals(date_, [suggested_m_id])
            suggestion = Suggestion(date=date_, time=time_, eligible_meals=";".join([m.id for m in eligible]),
                                    suggestion=suggested_m_id)
            db.session.add(suggestion)
            result.append(suggestion)
    db.session.commit()
    return result


def remove_suggestions(date_):
    Suggestion.query.filter(Suggestion.date == date_).delete()
    db.session.commit()

def update_suggestion(date_, time_, new_meal_id):
    Suggestion.query.filter_by(date=date_, time=time_).update({Suggestion.suggestion: new_meal_id})
    db.session.commit()


def recreate_suggestion(from_date, duration):
    sugg = Suggestion.query.filter(and_(Suggestion.date >= from_date, or_(Suggestion.committed == None, Suggestion.committed == False))).all()
    print("RETRY SUGGESTIONS: ", [(s.suggestion, s.committed) for s in sugg])
    Suggestion.query.filter(and_(Suggestion.date >= from_date, or_(Suggestion.committed == None, Suggestion.committed == False))).delete()
    return get_or_create_suggestions(from_date, duration)
