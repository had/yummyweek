from .. import db
from enum import Enum
from sqlalchemy.sql.expression import false


class MealTime(Enum):
    lunch = "Lunch"
    dinner = "Dinner"


class Suggestion(db.Model):
    __tablename__ = "suggestions"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    time = db.Column(db.Enum(MealTime))
    eligible_meals = db.Column(db.String)  # eligible meals are semi-column separated meal IDs
    suggestion = db.Column(db.String)  # suggestion is a single meal ID
    committed = db.Column(db.Boolean, default=False, server_default=false())
