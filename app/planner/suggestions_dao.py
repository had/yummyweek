from .models import Suggestion
from .. import db
from sqlalchemy.orm.exc import NoResultFound
from .meal_planning import suggest_meals


def get_or_create_suggestions(date_, duration):
    try:
        suggestion = Suggestion.query.filter_by(date=date_, duration=duration).one()
    except NoResultFound:
        suggestion = suggest_meals(date_, duration)
        db.session.add(suggestion)
        db.session.commit()
    return suggestion

def recreate_suggestion(date_, duration):
    Suggestion.query.filter_by(date=date_, duration=duration).delete()
    return get_or_create_suggestions(date_, duration)
