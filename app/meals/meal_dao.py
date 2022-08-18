from .models import Meal, MealType, MealElement, Recipe
import os
import itertools
from collections import defaultdict

checks = ["periodicity_d", "prep_time_m", "cooking_time_m"]


def sanity_check(m):
    if isinstance(m, Meal) and (getattr(m, "elements") or "BATCH" in (m.tags or "")):
        # if it's a meal and has elements or is for batch cooking, skip checks
        return True
    warn = ""
    for check in checks:
        if getattr(m, check) is None:
            warn += f" missing {check};"
    if warn:
        print(f"* Warning: {m.id}{warn}")
        return False
    return True


def read_mock_food(path):
    import pandas as pd
    import numpy as np
    print(f"Using mock food data from {path}")

    elements = []
    food_df = pd.read_excel(path, sheet_name="food_elements").replace({np.nan: None})
    for _, row in food_df.iterrows():
        d = row.to_dict()
        if d['active'] != 'Y':
            continue
        del d['active']
        elements.append(MealElement(**d))
    print(f"Found {len(elements)} meals")

    meals = []
    food_df = pd.read_excel(path, sheet_name="food_meals").replace({np.nan: None})
    for _, row in food_df.iterrows():
        d = row.to_dict()
        if d['active'] != 'Y':
            continue
        del d['active']
        d['meal_type'] = MealType(d['meal_type'])
        meals.append(Meal(**d))
    print(f"Found {len(meals)} meals")

    return list(filter(sanity_check, elements)), list(filter(sanity_check, meals))


def generate_available_meals(elements, meals):
    elements_by_type = defaultdict(list)
    for e in elements:
        elements_by_type[e.category].append(e)
    result = {}
    # create compounded meals
    for m in meals:
        if m.elements:
            elt_types = m.elements.split(';')
            meal_elements = [elements_by_type[t] for t in elt_types]
            compounded_meals = itertools.product(*meal_elements)
            for cm in compounded_meals:
                id_ = '+'.join([e.id for e in cm])
                name = ' & '.join([e.name for e in cm])
                prep_time = sum([e.prep_time_m for e in cm])
                cooking_time = sum([e.cooking_time_m for e in cm])
                periodicity = max([e.periodicity_d for e in cm])
                meal_type = MealType(m.meal_type)
                result[id_] = Meal(id=id_, name=name, meal_type=meal_type, prep_time_m=prep_time,
                                   cooking_time_m=cooking_time, periodicity_d=periodicity)
        else:
            # simple meal, just add it to the results
            result[m.id] = m
    return result


mock_food_env = os.environ.get('YUMMYWEEK_XLS')
mock_elements, mock_meals = read_mock_food(mock_food_env) if mock_food_env else ([], [
    Meal(id="COURGETTES", name="Courgettes", prep_time_m=20, cooking_time_m=25, meal_type=MealType.dinner,
         periodicity_d=8),
])

mock_meals_2 = generate_available_meals(mock_elements, mock_meals)


def parse_ingredients(ingredients_str):
    ingr_list = ingredients_str.split("|") if ingredients_str else []
    # TODO: further parse the quantities
    return ingr_list


def read_mock_recipes(path):
    import pandas as pd
    import numpy as np
    recipes = []
    recipes_df = pd.read_excel(path, sheet_name="food_recipes").replace({np.nan: None})
    for _, row in recipes_df.iterrows():
        d = row.to_dict()
        recipes.append(Recipe(**d))
    return {r.id: parse_ingredients(r.ingredients) for r in recipes}


mock_recipes = read_mock_recipes(mock_food_env) if mock_food_env else {}


def get_meal_elements():
    return mock_elements


def get_meals_unprocessed():
    return mock_meals


def get_meals():
    return mock_meals_2


def get_recipes():
    return mock_recipes


def ingredients_for_meals(meals):
    meals_or_elements = [e for m in meals for e in m.split('+')]
    recipes_dict = get_recipes()
    return [i for e in meals_or_elements for i in recipes_dict.get(e, [])]
