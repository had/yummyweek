import datetime
from collections.abc import Iterable
from datetime import timedelta
from random import choice

from app.meals.meal_history import get_history_range
from app.meals.meal_dao import ComposedMeal, get_all_meals
from app.meals.models import MealType
from app.planner.models import MealTime


class MealPlanner:
    def __init__(self, date_from: datetime.date, meals: dict[str, ComposedMeal] = None,
                 history: dict[datetime.date, list[ComposedMeal]] = None):
        self.date_from = date_from
        self.meals_dict = meals or get_all_meals()
        self.max_periodicity = max([m.periodicity_d for m in self.meals_dict.values() if m.periodicity_d])
        self.not_before_table: dict[str, datetime.date] = {}
        history: dict[datetime.date, list[ComposedMeal]] = history or get_history_range(date_from - timedelta(days=self.max_periodicity), date_from)
        for day, meals_that_day in history.items():
            self.process_dated_meals(day, meals_that_day)

    def process_dated_meals(self, date: datetime.date, meals: list[ComposedMeal]):
        for meal in meals:
            for dish in meal.dishes:
                self.not_before_table[dish.id] = date + timedelta(days=dish.periodicity_d)

    def get_eligible_meals(self, date: datetime.date) -> list[ComposedMeal]:
        return self._history_filter(date, self.meals_dict.values())

    # TODO: turn that into something more functional (yield and co)
    def _history_filter(self, date: datetime.date, meals: Iterable[ComposedMeal]) -> list[ComposedMeal]:
        def is_eligible_from_history(x):
            return x.id not in self.not_before_table or date >= self.not_before_table[x.id]

        history_eligible = []
        for meal in meals:
            if all([is_eligible_from_history(dish) for dish in meal.dishes]):
                history_eligible.append(meal)
        return history_eligible


def suggest_meal(date: datetime.date, time: MealTime, planner: MealPlanner):
    meals = planner.get_eligible_meals(date)
    if time == MealTime.lunch:
        eligible_meals = [m for m in meals if m.meal_moment != MealType.dinner]
    else:
        eligible_meals = [m for m in meals if m.meal_moment != MealType.lunch]
    suggestion = choice(eligible_meals).id
    return eligible_meals, suggestion
