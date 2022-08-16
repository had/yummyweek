from datetime import timedelta

from flask import Blueprint


def date_range(date_, nbdays):
    return [date_ + timedelta(days=d) for d in range(nbdays + 1)]

planner = Blueprint("planner", __name__)

from . import views
