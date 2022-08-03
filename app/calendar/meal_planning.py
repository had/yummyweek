from datetime import timedelta
from random import choice

from .meal_history import get_history_range
from ..meals.meal_list import get_meals
from ..meals.models import MealType


def _date_range(date_1, nbdays):
    return [date_1 + timedelta(days=d) for d in range(nbdays+1)]

def suggest_meal_date(date, history, all_meals):
    for days_since, past_meals in enumerate(reversed(history)):
        for past_meal in past_meals:
            if past_meal in all_meals and days_since <= all_meals[past_meal].periodicity_d:
                #print(f"Removing {past_meal} last eaten {days_since} ago")
                del all_meals[past_meal]
    try:
        lunch_meals = [m for m in all_meals.values() if m.meal_type != MealType.dinner]
        lunch_sugg = choice(lunch_meals).id
        dinner_meals = [m for m in all_meals.values() if (m.meal_type != MealType.lunch) and m.id != lunch_sugg]
        dinner_sugg = choice(dinner_meals).id
        print(f"{len(all_meals)} eligible meals left for {date} ({len(lunch_meals)} lunches, {len(dinner_meals)} dinners)")
        res = [lunch_sugg, dinner_sugg]
        print("RES", res)
        return res
    except:
        return []

def suggest_meals(date, duration):
    all_meals = {m.id:m for m in get_meals() if m.periodicity_d}
    print(f"{len(all_meals)} meals have valid periodicity")
    max_periodicity = max([m.periodicity_d for m in all_meals.values()])
    history = get_history_range(date-timedelta(days=max_periodicity), date)
    results = {}
    for day in _date_range(date, duration):
        suggestion = suggest_meal_date(day, history, all_meals.copy())
        results[day] = suggestion
        history.append(suggestion)
    print(results)
    return results
