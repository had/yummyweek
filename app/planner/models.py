from .. import db


class Suggestion(db.Model):
    __tablename__ = "suggestions"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    duration = db.Column(db.Integer)
    lunches = db.Column(db.String)  # lunches and dinners are semi-column separated meal IDs
    dinners = db.Column(db.String)
