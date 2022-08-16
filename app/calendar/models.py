from .. import db


class MealHistory(db.Model):
    __tablename__ = "meal_history"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    meal = db.Column(db.String, db.ForeignKey('meals.id'))
