import calendar
import datetime
from itertools import groupby

from app.meals.meal_dao import ComposedMeal
from app.meals.models import MealHistory, MealType
from app import db


def _last_day_of_month(year, month):
    return calendar.monthrange(year, month)[1]


def get_history_range(range_from: datetime.date, range_to: datetime.date) -> dict[datetime.date, list[ComposedMeal]]:
    rows = MealHistory.query.filter(MealHistory.date.between(range_from, range_to)).order_by(MealHistory.date).all()
    v = {}
    for d, meals in groupby(rows, key=lambda r: r.date):
        v[d] = [ComposedMeal.from_composed_id(m.meal, MealType.both) for m in meals]
    return v


def get_history(year, month) -> dict[datetime.date, list[ComposedMeal]]:
    range_1 = datetime.date(year, month, 1)
    range_2 = datetime.date(year, month, _last_day_of_month(year, month))
    return get_history_range(range_1, range_2)


def set_history(year, month, day, meals: str):
    date = datetime.date(year, month, day)
    MealHistory.query.filter_by(date=date).delete()
    for meal in meals:
        db.session.add(MealHistory(date=date, meal=meal))
    db.session.commit()
