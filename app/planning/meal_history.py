import calendar
import datetime
from itertools import groupby

from .models import MealHistory
from .. import db


def _last_day_of_month(year, month):
    return calendar.monthrange(year, month)[1]


def get_history(year, month):
    range_1 = datetime.date(year, month, 1)
    range_2 = datetime.date(year, month, _last_day_of_month(year, month))
    rows = MealHistory.query.filter(MealHistory.date.between(range_1, range_2)).order_by(MealHistory.date).all()
    v = [[] for _ in range(_last_day_of_month(year, month) + 1)]
    for d, meals in groupby(rows, key=lambda r: r.date):
        v[d.day] = [m.meal for m in meals]
    return v


def set_history(year, month, day, meals):
    date = datetime.date(year, month, day)
    MealHistory.query.filter_by(date=date).delete()
    for meal in meals:
        db.session.add(MealHistory(date=date, meal=meal))
    db.session.commit()


# Simple memory-based history for development purpose (no DB)
class MonthDict(dict):
    def __missing__(self, key):
        (year, month) = key
        v = [[] for _ in range(_last_day_of_month(year, month) + 1)]
        self[key] = v
        return v


history = MonthDict()


def get_history_mock(year, month):
    return history[(year, month)]


def set_history_mock(year, month, day, meals):
    l = history[(year, month)]
    l[day] = meals
