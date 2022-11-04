from .. import db
from enum import Enum


class MealType(Enum):
    lunch = "Lunch"
    dinner = "Dinner"
    both = "Both"
    batch_cooking = "Batch"


class Dish(db.Model):
    __tablename__ = "dishes"
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    elements = db.Column(db.String)
    prep_notes = db.Column(db.String)
    prep_time_m = db.Column(db.Integer, default=0, nullable=False)
    cooking_notes = db.Column(db.String)
    cooking_time_m = db.Column(db.Integer, default=0, nullable=False)
    cooking_time_comments = db.Column(db.String)
    periodicity_d = db.Column(db.Integer, default=0, nullable=False)
    tags = db.Column(db.String)
    # note: this is a pipe-separated string with list and quantity of ingredients (see unit-tests)
    ingredients = db.Column(db.String)

    def __repr__(self):
        params = ", ".join([f"{a}={getattr(self, a)}" for a in ["id", "name", "category", "elements", "prep_time_m",
                                                                "cooking_time_m", "periodicity_d"]])
        return f"Dish({params})"


class Ingredient(db.Model):
    __tablename__ = "ingredients"
    ingredient = db.Column(db.String, primary_key=True)
    category = db.Column(db.String)


class MealHistory(db.Model):
    __tablename__ = "meal_history"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    meal = db.Column(db.String)
