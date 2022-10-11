import datetime
from datetime import timedelta
from random import choice

from app.meals.meal_history import get_history_range
from app.meals.meal_dao import get_meals, get_all_dishes
from app.meals.models import MealType, Dish
from app.planner.models import MealTime


def suggest_meal(date, time, planner):
    meals = planner.get_eligible_meals(date)
    if time == MealTime.lunch:
        eligible_meals = [m for m in meals if m.meal_type != MealType.dinner]
    else:
        eligible_meals = [m for m in meals if m.meal_type != MealType.lunch]
    suggestion = choice(eligible_meals).id
    return eligible_meals, suggestion


class MealPlanner:
    def __init__(self, date_from: datetime.date, dishes: list[Dish] = None, meals: dict[str, Dish] = None, history=None):
        self.date_from = date_from
        self.dishes = {d.id: d for d in (dishes or get_all_dishes())}
        self.meals_dict = meals or get_meals()
        self.max_periodicity = max([m.periodicity_d for m in self.meals_dict.values() if m.periodicity_d])
        self.not_before_table = {}
        history = history or get_history_range(date_from - timedelta(days=self.max_periodicity), date_from)
        for day, meals_that_day in history.items():
            self.process_dated_meals(day, meals_that_day)

    def process_dated_meals(self, date, meals):
        for m_id in meals:
            if m_id in self.dishes:
                elt = self.dishes[m_id]
                self.not_before_table[elt.id] = date + timedelta(days=elt.periodicity_d)
            elif "+" in m_id:
                # compounded meal, need to decompose the elements
                meal_elts = [self.dishes[elt_id] for elt_id in m_id.split("+")]
                for elt in meal_elts:
                    self.not_before_table[elt.id] = date + timedelta(days=elt.periodicity_d)
            else:
                meal = self.meals_dict.get(m_id)
                if not meal:
                    print(f"Warning: cannot find {m_id} in current list of meals")
                    continue
                self.not_before_table[meal.id] = date + timedelta(days=meal.periodicity_d)

    def get_eligible_meals(self, date):
        return self._history_filter(date, self.meals_dict.values())

    # TODO: turn that into something more functional (yield and co)
    def _history_filter(self, date, meals):
        def is_eligible_from_history(x):
            return x.id not in self.not_before_table or date >= self.not_before_table[x.id]

        history_eligible = []
        for m in meals:
            if "+" in m.id:
                # compounded meal, need to decompose the elements
                meal_elts = [self.elements[elt_id] for elt_id in m.id.split("+")]
                if all([is_eligible_from_history(elt) for elt in meal_elts]):
                    history_eligible.append(m)
            else:
                if is_eligible_from_history(m):
                    history_eligible.append(m)
        return history_eligible
