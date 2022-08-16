from datetime import timedelta
from random import choice

from app.calendar.meal_history import get_history_range
from app.meals.meal_dao import get_meals, get_meal_elements
from app.meals.models import MealType
from app.planner import date_range
from app.planner.models import Suggestion


def suggest_meal_date(date, planner):
    meals = planner.get_eligible_meals(date)
    lunch_meals = [m for m in meals if m.meal_type != MealType.dinner]
    lunch_sugg = choice(lunch_meals).id
    dinner_meals = [m for m in meals if (m.meal_type != MealType.lunch) and m.id != lunch_sugg]
    dinner_sugg = choice(dinner_meals).id
    res = [lunch_sugg, dinner_sugg]
    return res


def suggest_meals(date_, duration):
    planner = MealPlanner(date_)
    lunches, dinners = [], []
    for day in date_range(date_, duration):
        # TODO fix bug where we can suggest the same meal or elements for lunch and dinner in a same day
        suggestion = suggest_meal_date(day, planner)
        lunches.append(suggestion[0])
        dinners.append(suggestion[1])
        print("Suggesting: ", suggestion)
        planner.process_dated_meals(day, suggestion)
    sugg = Suggestion(date=date_, duration=duration, lunches=";".join(lunches), dinners=";".join(dinners))
    return sugg


class MealPlanner:
    def __init__(self, date_from, elements=None, meals=None, history=None):
        self.date_from = date_from
        self.elements = {e.id: e for e in (elements or get_meal_elements())}
        self.meals_dict = meals or get_meals()
        self.max_periodicity = max([m.periodicity_d for m in self.meals_dict.values() if m.periodicity_d])
        self.not_before_table = {}
        history = history or get_history_range(date_from - timedelta(days=self.max_periodicity), date_from)
        for day, meals_that_day in history.items():
            self.process_dated_meals(day, meals_that_day)

    def process_dated_meals(self, date, meals):
        for m_id in meals:
            if m_id in self.elements:
                elt = self.elements[m_id]
                self.not_before_table[elt.id] = date + timedelta(days=elt.periodicity_d)
            elif "+" in m_id:
                # compounded meal, need to decompose the elements
                meal_elts = [self.elements[elt_id] for elt_id in m_id.split("+")]
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
