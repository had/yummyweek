from .. import db
from enum import Enum

class MealType(Enum):
    lunch = "Lunch"
    dinner = "Dinner"
    both = "Both"
    batch_cooking = "Batch"

class Meal(db.Model):
    __tablename__ = "meals"
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    prep_notes = db.Column(db.String)
    prep_time_m = db.Column(db.Integer)
    cooking_notes = db.Column(db.String)
    cooking_time_m = db.Column(db.Integer)
    meal_type = db.Column(db.Enum(MealType))
    periodicity_d = db.Column(db.Integer)

